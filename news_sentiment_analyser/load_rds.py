"""A script to load the dataframe into the database."""

from datetime import datetime

import pandas as pd
from psycopg2.extras import execute_values

from database_functions import create_connection, get_topic_dict


def load(articles: pd.DataFrame) -> None:
    """Loads all the articles and article_topic_assignment into the RDS tables."""
    if not articles.empty:
        article_id_dict = insert_into_articles(articles)
        processed_df = process_df_for_assignment_insert(
            articles, article_id_dict)
        insert_into_assignment(processed_df)


def insert_into_articles(articles: pd.DataFrame) -> dict:
    """Bulk inserts the articles into the article table 
    and returns  dictionary of article title to id."""
    article_df = articles[['title', 'content', 'title_polarity_score',
                           'content_polarity_score',
                           'source_id', 'published', 'link']]
    params = [tuple(x) for x in article_df.values]
    article_insert_query = """
    INSERT INTO article (
        article_title, article_content, title_polarity_score, content_polarity_score, 
        source_id, date_published, article_url
    ) VALUES %s
    ON CONFLICT (article_title, source_id, date_published) DO NOTHING
    RETURNING article_id, article_title;
    """
    with create_connection() as conn:
        with conn.cursor() as cur:
            execute_values(cur, article_insert_query, params)
            inserted_ids = cur.fetchall()
        conn.commit()
    article_id_dict = {row['article_title']: row['article_id']
                       for row in inserted_ids}

    return article_id_dict


def process_df_for_assignment_insert(articles: pd.DataFrame, article_id_dict: dict) -> pd.DataFrame:
    """Processes the dataframe to be inserted into the article_topic_assignment table."""
    topic_dict = get_topic_dict()
    article_df = articles[['topics', 'title']]
    article_df = article_df.explode('topics')
    article_df['topic_id'] = article_df['topics'].map(topic_dict)
    article_df['article_id'] = article_df['title'].map(article_id_dict)
    article_df = article_df[['topic_id', 'article_id']]

    return article_df


def insert_into_assignment(articles: pd.DataFrame) -> None:
    """Bulk inserts the article-topic into the article_topic_assignment table."""
    params = articles.to_numpy().tolist()
    params = [(int(topic_id), int(article_id))
              for topic_id, article_id in params]
    assignment_insert_query = """
    INSERT INTO article_topic_assignment (topic_id, article_id) VALUES %s
    ON CONFLICT (topic_id, article_id) DO NOTHING;
    """
    with create_connection() as conn:
        with conn.cursor() as cur:
            execute_values(cur, assignment_insert_query, params)
        conn.commit()


if __name__ == "__main__":
    fake_data = {
        "title": [
            "Trump Criticizes 2024 Election Process",
            "Harris Advocates for Climate Change Action",
            "Natural Disaster Strikes Coastal City",
            "Supreme Court Rules on Abortion Laws"
        ],
        "content": [
            "In a recent rally, Donald Trump h...",
            "Vice President Kamala Harris urged the...",
            "A devastating hurricane hit the...",
            "The Supreme Court ruled on..."
        ],
        "polarity_score": [0.1, 0.8, -0.4, -0.2],
        "source_id": [1, 2, 1, 2],
        "date_published": [
            datetime(2023, 8, 12),
            datetime(2024, 3, 5),
            datetime(2024, 1, 22),
            datetime(2023, 10, 14)
        ],
        "article_url": [
            "https://example.com/trump-2024-criticism",
            "https://example.com/harris-climate-change",
            "https://example.com/natural-disaster-coast",
            "https://example.com/supreme-court-abortion"
        ],
        "topics": [
            ['Donald Trump', '2024 Presidential Election'],
            ['Kamala Harris', 'Climate Change'],
            ['Natural Disaster'],
            ['Abortion', 'Crime and Law Enforcement']
        ]
    }

    fake_articles = pd.DataFrame(fake_data)

    load(fake_articles)
