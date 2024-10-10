"""Some functions for interacting with the RDS."""
from os import environ as ENV
from datetime import datetime, timedelta

import pandas as pd
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


def get_avg_polarity_by_topic_and_source_yesterday():
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    query = f"""
        SELECT 
            t.topic_name,
            s.source_name,
            AVG(a.content_polarity_score) AS avg_polarity_score
        FROM article_topic_assignment ata
        JOIN article a ON ata.article_id = a.article_id
        JOIN topic t ON ata.topic_id = t.topic_id
        JOIN source s ON a.source_id = s.source_id
        WHERE a.date_published = %s
        GROUP BY t.topic_name, s.source_name
        ORDER BY t.topic_name, s.source_name;
    """

    with create_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (yesterday,))
            data = cur.fetchall()
    return pd.DataFrame(data)
