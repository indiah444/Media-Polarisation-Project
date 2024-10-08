'''Generates dummy data'''
from os import environ as ENV
import random
from faker import Faker

from dotenv import load_dotenv
import psycopg2
from psycopg2 import extras

TOPICS = ["Trump", 
          "Kamala", 
          "Israel-Gaza",
          "Hurricanes", 
          "Natural disasters",
          "World news",
          "Climate change", 
          "Voting",
          ]


FOX_HEADLINES = {
    "Supreme Court denies Biden administration appeal over federal emergency abortion requirement in Texas":
    ["Supreme Court decisions", "Justice system"],

    "Massive wildfires rage across California amid intense heatwave, thousands evacuated":
    ["Natural disasters"],

    "Kamala Harris faces backlash after controversial comments on immigration policies":
    ["Kamala"],

    "US inflation hits 40-year high, causing concerns for the economy":
    ["Economics", "Inflation", "Cost of living"],

    "Russia-Ukraine war: Latest developments and international reactions":

    ["War", "Russia-Ukraine", "World news"],

    "Supreme Court takes on major gun control case with national implications":

    ["Supreme Court decisions", "Guns", "Justice system"]
}


def connect():
    '''Return a connection to the RDS database.'''
    load_dotenv()
    return psycopg2.connect(dbname=ENV["DB_NAME"],
                            host=ENV["DB_HOST"],
                            user=ENV["DB_USER"],
                            port=ENV["DB_PORT"],
                            password=ENV["DB_PASSWORD"],
                            cursor_factory=psycopg2.extras.RealDictCursor)


def generate_fake_topics() -> list[tuple]:
    '''Generates fake topic rows containing:
        -topic_id
        -topic_name
    '''
    return [(i+1, t) for i, t in enumerate(TOPICS)]


def generate_fake_subscribers(fake: Faker, num: int) -> list[tuple]:
    '''Generates fake subscribers. 
    Returns a list of tuples containing:
        - subscriber_id
        - subscriber_email
        - subscriber_first_name
        - subscriber_surname  
    '''

    subscribers = []

    for i in range(1, num+1):
        sub_id = i
        email = fake.unique.email()
        first_name = fake.first_name()
        last_name = fake.last_name()
        subscribers.append((sub_id, email, first_name, last_name))
    return subscribers


def generate_fake_articles(faker: Faker, num_articles: int, source_id: int, source_headlines: list) -> list[tuple]:
    '''Generates fake article table entries.
    Returns a list of tuples containing:
        - article_id
        - article_title
        - polarity_score
        - source_id
        - date_published
        - article_url
    '''

    articles = []

    for i in range(1, min(len(source_headlines), num_articles) + 1):
        article_id = i

        article_title = source_headlines[i-1]
        
        polarity_score = random.triangular(-1.0, 0.0, -0.5)
        date_published = faker.date_time_between(
            start_date='-5d')
        article_url = faker.url()
        articles.append((article_id, article_title, polarity_score,
                        source_id, date_published, article_url))
    return articles

def insert_data_to_db(conn, fake_topics: list[tuple], fake_subs: list[tuple], fake_articles: list[tuple]):
    '''Inserts fake data into the database'''
    with conn.cursor() as cursor:

        extras.execute_values(cursor, 
            "INSERT INTO topic (topic_id, topic_name) VALUES %s", 
            fake_topics)

        extras.execute_values(cursor, 
            "INSERT INTO subscribers (subscriber_id, subscriber_email, subscriber_first_name, subscriber_surname) VALUES %s", 
            fake_subs)


        extras.execute_values(cursor, 
            "INSERT INTO article (article_id, article_title, polarity_score, source_id, date_published, article_url) VALUES %s", 
            fake_articles)

        extras.execute_values(cursor, 
            "INSERT INTO subscriber_topic_assignments (subscriber_topic_assignment_id, subscriber_id, topic_id) VALUES %s", 
            generate_fake_assignment(fake_subs, fake_topics, 15))
        

        extras.execute_values(cursor, 
            "INSERT INTO article_topic_assignment (subscriber_topic_assignment_id, topic_id, article_id) VALUES %s", 
            generate_fake_assignment(fake_topics, fake_articles, 18))
        
        conn.commit()

if __name__ == "__main__":
    f = Faker()
    subs = generate_fake_subscribers(f, 3)
    topics = generate_fake_topics()

    fox_headlines = list(FOX_HEADLINES.keys())
    articles = generate_fake_articles(f, 12, 1, fox_headlines)

    with connect() as connection:
        insert_data_to_db(connection,topics,subs, articles)
