'''Generates dummy data'''
from faker import Faker
import random
from os import environ as ENV
from dotenv import load_dotenv
import psycopg2

TOPICS = ["Immigration", "Justice system", "P Diddy",
          "Supreme Court decisions", "Religion",
          "Natural disasters", "Hurricane Helene", "World news",
          "Climate change", "China", "Education", "Woke activism", "Crime and law enforcement", "Guns", "Economics",
          "Recession", "Inflation", "Cost of living", "Politics",
          "Trump", "Kamala", "Voting", "Tim Walz", "JD Vance",
          "War", "Israel-Gaza", "Russia-Ukraine", "Iran", "Lebanon",
          "Social", "Race relations", "LGBTQ+ issues", "Abortion"
          ]


FOX_HEADLINES = {
    "Mexican mayor's severed head placed atop pick-up truck 6 days after taking office": ["World news", "Immigration"],

    "Supreme Court denies Biden administration appeal over federal emergency abortion requirement in Texas":
    ["Supreme Court decisions", "Justice system"],

    "P Diddy sued by former employee over workplace harassment": ["P Diddy", "Justice system"],

    "Massive wildfires rage across California amid intense heatwave, thousands evacuated":
    ["Natural disasters", "Climate change"],

    "Kamala Harris faces backlash after controversial comments on immigration policies":
    ["Politics", "Kamala", "Immigration"],

    "China's new military drills raise tensions in the South China Sea": ["China", "World news"],

    "Justice Department investigates police handling of race-related protests in Minneapolis":
    ["Justice system", "Race relations", "Crime and law enforcement"],

    "US inflation hits 40-year high, causing concerns for the economy":
    ["Economics", "Inflation", "Cost of living"],

    "Russia-Ukraine war: Latest developments and international reactions":
    ["War", "Russia-Ukraine", "World news"],

    "Supreme Court takes on major gun control case with national implications":
    ["Supreme Court decisions", "Guns", "Justice system"]
}


def connect() -> Connection:
    '''Return a connection to redshift.'''

    return psycopg2.connect(dbname=db_name,
                            host=ENV["DATABASE_HOST"],
                            user=ENV["DATABASE_USERNAME"],
                            port=ENV["DATABASE_PORT"],
                            password=ENV["DATABASE_PASSWORD"],
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


def generate_fake_assignment(table1: list[tuple], table2: list[tuple], num_assignments: int) -> list[tuple]:
    '''Generates random assignment table rows.
    table1 and table2 are lists of rows in the mapped tables. 
    It's assumed that the first item in each row is the id.'''

    assignments = []
    for i in range(1, num_assignments + 1):
        subscriber = random.choice(table1)
        topic = random.choice(table2)

        assignments.append((i, subscriber[0], topic[0]))
    return assignments


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
        source_id = 1
        polarity_score = random.triangular(-1.0, 0.0, -0.5)
        date_published = faker.date_time_between(
            start_date='-5d')
        article_url = faker.url()
        articles.append((article_id, article_title, polarity_score,
                        source_id, date_published, article_url))
    return articles


if __name__ == "__main__":
    f = Faker()
    fake_subs = generate_fake_subscribers(f, 3)
    fake_topics = generate_fake_topics()

    fake_subs_topics = generate_fake_assignment(
        fake_subs, fake_topics, 12)

    fox_headlines = list(FOX_HEADLINES.keys())
    fake_articles = generate_fake_articles(f, 12, 1, fox_headlines)
    print(fake_articles)
