"""Some functions for interacting with the RDS."""

from os import environ as ENV
from datetime import datetime, timedelta


from psycopg2.extensions import connection, cursor
from psycopg2.extras import RealDictCursor
from psycopg2 import connect
from dotenv import load_dotenv
import pandas as pd


def create_connection() -> connection:
    """Creates a connection to the RDS with postgres."""

    load_dotenv()
    conn = connect(dbname=ENV["DB_NAME"], user=ENV["DB_USER"],
                   host=ENV["DB_HOST"], password=ENV["DB_PASSWORD"],
                   port=ENV["DB_PORT"],
                   cursor_factory=RealDictCursor)

    return conn


def get_cursor(conn: connection) -> cursor:
    """Return cursor object to execute sql commands"""

    return conn.cursor()


def get_avg_polarity_last_week():
    """
    Returns a dataframe of  average sentiment for each topic and score
    in the last week.
    """

    last_week = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    today = datetime.now().strftime('%Y-%m-%d')

    query = """
        SELECT t.topic_name, s.source_name,
        AVG(a.content_polarity_score) AS avg_polarity_score,
        COUNT(a.article_id) AS article_count
        FROM article_topic_assignment ata
        JOIN article a ON ata.article_id = a.article_id
        JOIN topic t ON ata.topic_id = t.topic_id
        JOIN source s ON a.source_id = s.source_id
        WHERE a.date_published BETWEEN %s AND %s
        GROUP BY t.topic_name, s.source_name
        ORDER BY t.topic_name, s.source_name;
    """

    with create_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute(query, (last_week, today))
            data = cur.fetchall()

    return pd.DataFrame(data)


def get_weekly_subscribers() -> list[str]:
    """Returns the emails of subscribers for weekly emails."""

    query = """
        SELECT subscriber_email 
        FROM subscriber
        WHERE weekly = TRUE
        """
    with create_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute(query)
            data = cur.fetchall()
    if not data:
        return []

    return [subscriber['subscriber_email'] for subscriber in data]
