"""Some functions for interacting with the RDS."""
from os import environ as ENV

from psycopg2.extras import RealDictCursor
from psycopg2 import connect
from psycopg2.extensions import connection
from dotenv import load_dotenv


def create_connection() -> connection:
    """Creates a connection to the RDS with postgres."""
    load_dotenv()
    conn = connect(dbname=ENV["DB_NAME"], user=ENV["DB_USER"],
                   host=ENV["DB_HOST"], password=ENV["DB_PASSWORD"],
                   port=ENV["DB_PORT"],
                   cursor_factory=RealDictCursor)

    return conn


def get_topic_names() -> list[str]:
    """Returns a list of topic names."""
    with create_connection() as conn:
        query = """SELECT topic_name FROM topic;"""
        with conn.cursor() as cur:
            cur.execute(query)
            res = cur.fetchall()

    return [topic['topic_name'] for topic in res]


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
        select_data = """SELECT t.topic_name, s.source_name, a.content_polarity_score, a.title_polarity_score, a.date_published FROM article a
        INNER JOIN article_topic_assignment ata ON a.article_id = ata.article_id 
        INNER JOIN topic t ON ata.topic_id = t.topic_id 
        INNER JOIN source s ON a.source_id = s.source_id
        WHERE t.topic_name = %s 
        """
        with conn.cursor() as curr:
            curr.execute(select_data,(topic_name, ))
            res = curr.fetchall()

    return res
