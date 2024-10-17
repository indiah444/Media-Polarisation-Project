# pylint: disable=R0801

"""Some functions for interacting with the RDS."""

from os import environ as ENV

from psycopg2.extras import RealDictCursor
from psycopg2 import connect
from psycopg2.extensions import connection
from dotenv import load_dotenv
import pandas as pd
import streamlit as st

from verify_identity import check_and_verify_email


def create_connection() -> connection:
    """Creates a connection to the RDS with postgres."""
    load_dotenv()
    conn = connect(dbname=ENV["DB_NAME"], user=ENV["DB_USER"],
                   host=ENV["DB_HOST"], password=ENV["DB_PASSWORD"],
                   port=ENV["DB_PORT"],
                   cursor_factory=RealDictCursor)

    return conn


@st.cache_data
def get_topic_names() -> list[str]:
    """Returns a list of topic names."""
    with create_connection() as conn:
        query = """SELECT topic_name FROM topic;"""
        with conn.cursor() as cur:
            cur.execute(query)
            res = cur.fetchall()

    return [topic['topic_name'] for topic in res]


@st.cache_data
def get_topic_dict() -> dict:
    """Returns a dictionary of topic name to its id."""
    with create_connection() as conn:
        query = """SELECT * FROM topic;"""
        with conn.cursor() as cur:
            cur.execute(query)
            res = cur.fetchall()
    return {topic['topic_name']: topic['topic_id'] for topic in res}


def get_scores_topic(topic_name: str) -> dict:
    """Returns a dictionary containing the polarity scores for a given topic """

    topic_name = topic_name.strip().title()
    with create_connection() as conn:
        select_data = """
        SELECT t.topic_name, s.source_name, a.content_polarity_score, a.title_polarity_score, a.date_published 
        FROM article a
        INNER JOIN article_topic_assignment ata ON a.article_id = ata.article_id 
        INNER JOIN topic t ON ata.topic_id = t.topic_id 
        INNER JOIN source s ON a.source_id = s.source_id
        WHERE t.topic_name = %s 
        """
        with conn.cursor() as curr:
            curr.execute(select_data, (topic_name, ))
            res = curr.fetchall()

    return res


def get_average_score_per_source_for_a_topic(topic_id):
    """Get average score for a topic by source in the last week."""
    query = """
        SELECT s.source_name,
        AVG(a.content_polarity_score) AS avg_polarity_score,
        COUNT(a.article_id) AS article_count
        FROM article_topic_assignment ata
        JOIN article a ON ata.article_id = a.article_id
        JOIN source s ON a.source_id = s.source_id
        WHERE ata.topic_id = %s 
        GROUP BY s.source_name
    """

    with create_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (topic_id, ))
            data = cur.fetchall()

    return pd.DataFrame(data)


@st.cache_data
def get_title_and_content_data_for_a_topic(topic_id):
    """Get article and content scores for the last week."""
    query = """
        SELECT a.article_title, a.title_polarity_score,
        a.content_polarity_score, s.source_name
        FROM article_topic_assignment ata
        JOIN article a ON ata.article_id = a.article_id
        JOIN source s ON a.source_id = s.source_id
        WHERE ata.topic_id = %s 
    """

    with create_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (topic_id,))
            data = cur.fetchall()

    return pd.DataFrame(data)


@st.cache_data
def get_subscriber_emails() -> list[str]:
    """Returms a list of subscriber emails."""
    query = """
        SELECT subscriber_email from subscriber;
    """
    with create_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            data = cur.fetchall()
    if data:
        return [subscriber['subscriber_email'] for subscriber in data]
    return []


def updates_subscriber(first_name: str, surname: str, email: str, daily: bool, weekly: bool):
    """Updates a subscription preference."""
    query = """
            UPDATE subscriber
            SET subscriber_first_name = %s,
            subscriber_surname = %s,
            daily = %s,
            weekly = %s
            WHERE subscriber_email = %s"""
    with create_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (first_name, surname, daily, weekly, email))
        conn.commit()


def add_new_subscriber(first_name: str, surname: str, email: str, daily: bool, weekly: bool):
    """Adds a new subscriber."""
    check_and_verify_email(email)
    query = """
            INSERT INTO subscriber 
            (subscriber_email, subscriber_first_name, subscriber_surname, daily, weekly)
            VALUES (%s, %s, %s, %s, %s)"""
    with create_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (email, first_name, surname, daily, weekly))
        conn.commit()


def remove_subscription(email: str):
    """Removes a subscriber."""
    query = """
            DELETE FROM subscriber
            WHERE subscriber_email = %s"""
    with create_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (email, ))
        conn.commit()


def get_avg_polarity_all_topics():
    """Returns a dataframe of  average sentiment for each topic and score
    in the last week."""

    query = """
        SELECT t.topic_name, s.source_name,
        AVG(a.content_polarity_score) AS avg_polarity_score,
        COUNT(a.article_title) AS article_count
        FROM article_topic_assignment ata
        JOIN article a ON ata.article_id = a.article_id
        JOIN topic t ON ata.topic_id = t.topic_id
        JOIN source s ON a.source_id = s.source_id
        GROUP BY t.topic_name, s.source_name
        ORDER BY t.topic_name, s.source_name;
    """

    with create_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            data = cur.fetchall()

    return pd.DataFrame(data)


@st.cache_data
def get_all_article_content():
    """Returns all article content from the database, along with their
    topics."""

    with create_connection() as conn:
        query = """
        SELECT article.article_id, article.article_content, source.source_name, article.date_published, 
               topic.topic_name
        FROM article
        JOIN source ON article.source_id = source.source_id
        LEFT JOIN article_topic_assignment ON article.article_id = article_topic_assignment.article_id
        LEFT JOIN topic ON article_topic_assignment.topic_id = topic.topic_id;
        """
        with conn.cursor() as cur:
            cur.execute(query)
            articles = cur.fetchall()

    return articles
