"""Generates dummy data"""

from os import environ as ENV
import random

from faker import Faker
from dotenv import load_dotenv
import psycopg2
from psycopg2 import extras

TOPICS = [
    "Trump",
    "Kamala",
    "2024 Presidential Election",
    "Climate Change",
    "Natural Disasters",
    "Abortion",
    "Crime and Law Enforcement",
    "Guns"
]

FOX_HEADLINES = {
    "Trump announces his candidacy for the 2024 Presidential Election":
    ["Trump", "2024 Presidential Election"],
    "Kamala Harris addresses concerns over climate change at the international summit":
    ["Kamala", "Climate Change"],
    "Latest polls show Trump leading the race for the 2024 Presidential Election":
    ["Trump", "2024 Presidential Election"],
    "Severe floods devastate parts of the Midwest as climate change impacts intensify":
    ["Natural Disasters", "Climate Change"],
    "New study reveals the effects of climate change on hurricane patterns":
    ["Climate Change", "Natural Disasters"],
    "Supreme Court hears landmark case on abortion rights":
    ["Abortion", "Crime and Law Enforcement"],
    "Crime rates soar in major cities as policing practices come under scrutiny":
    ["Crime and Law Enforcement"],
    "Gun violence in America reaches alarming levels as calls for reform grow":
    ["Guns", "Crime and Law Enforcement"]
}


def connect(dbname, host: str, user: str, port: str, password: str):
    """Return a connection to the RDS database."""

    return psycopg2.connect(dbname=dbname,
                            host=host,
                            user=user,
                            port=port,
                            password=password,
                            cursor_factory=psycopg2.extras.RealDictCursor)


def generate_fake_subscribers(fake: Faker, num: int) -> list[tuple]:
    """Generates fake subscribers."""

    subscribers = []

    for _ in range(1, num+1):
        email = fake.unique.email()
        first_name = fake.first_name()
        last_name = fake.last_name()
        subscribers.append((email, first_name, last_name))
    return subscribers


def generate_fake_articles(
        faker: Faker, num_articles: int, source_id: int,
        source_headlines: list
) -> list[tuple]:
    """Generates fake article table entries."""

    rows = []

    for i in range(1, min(len(source_headlines), num_articles) + 1):
        article_title = source_headlines[i-1]
        polarity_score = random.triangular(-1.0, 0.0, -0.5)
        date_published = faker.date_time_between(
            start_date='-5d')
        article_url = faker.url()

        rows.append((article_title, polarity_score,
                     source_id, date_published, article_url))
    return rows


def generate_article_topic_assignment(headlines: dict, ordered_topics: list) -> list[tuple]:
    """Generates fake article_topic_assignment table rows."""

    assignments = []

    for article_id, (_, all_topics) in enumerate(headlines.items(), start=1):

        for topic in all_topics:

            topic_id = ordered_topics.index(topic) + 1

            assignments.append((topic_id, article_id))

    return assignments


def insert_data_to_db(conn, fake_subs: list[tuple], fake_articles: list[tuple],
                      assignments: list[tuple]):
    """Inserts fake data into the database"""

    with conn.cursor() as cursor:

        extras.execute_values(cursor, """
            INSERT INTO subscriber
            (subscriber_email, subscriber_first_name, 
            subscriber_surname) 
            VALUES %s""", fake_subs)

        extras.execute_values(cursor, """INSERT INTO article (article_title,
            polarity_score, source_id, date_published, article_url)
            VALUES %s""", fake_articles)

        extras.execute_values(cursor, """
            INSERT INTO article_topic_assignment 
            (topic_id, article_id) 
            VALUES %s""", assignments)

        conn.commit()


if __name__ == "__main__":
    load_dotenv()
    f = Faker()
    subs = generate_fake_subscribers(f, 3)

    fox_headlines = list(FOX_HEADLINES.keys())

    articles = generate_fake_articles(f, 12, 1, fox_headlines)

    article_assignments = generate_article_topic_assignment(
        FOX_HEADLINES, TOPICS)

    with connect(ENV["DB_NAME"],
                 ENV["DB_HOST"],
                 ENV["DB_USER"],
                 ENV["DB_PORT"],
                 ENV["DB_PASSWORD"]) as connection:
        insert_data_to_db(connection, subs,
                          articles, article_assignments)
