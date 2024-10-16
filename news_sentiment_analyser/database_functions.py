"""Functions that interact with the database"""

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


def get_source_dict() -> dict:
    """Returns a dictionary of source name  to its id."""
    with create_connection() as conn:
        query = """SELECT source_name, source_id FROM source;"""
        with conn.cursor() as cur:
            cur.execute(query)
            res = cur.fetchall()
    return {source['source_name']: source['source_id'] for source in res}


def get_article_titles() -> list[str]:
    """Returns a list of article titles."""
    with create_connection() as conn:
        query = """SELECT article_title FROM article;"""
        with conn.cursor() as cur:
            cur.execute(query)
            res = cur.fetchall()
    if res:
        return [article['article_title'] for article in res]
    return []


if __name__ == "__main__":
    print(get_article_titles())
