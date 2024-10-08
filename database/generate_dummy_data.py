'''Generates dummy data'''
from faker import Faker
import random

TOPICS = ["Immigration", "Justice system", "P Diddy",
          "Supreme Court decisions", "Religion",
          "Natural disasters", "Hurricane Helene", "World news",
          "Climate change", "China", "Education", "Woke activism", "Crime and law enforcement", "Guns", "Economics",
          "Recession", "Inflation", "Cost of living", "Politics",
          "Trump", "Kamala", "Voting", "Tim Walz", "JD Vance",
          "War", "Israel-Gaza", "Russia-Ukraine", "Iran", "Lebanon",
          "Social", "Race relations", "LGBTQ+ issues", "Abortion"
          ]


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


def generate_fake_subscriber_topic_assignments(subscribers: list[tuple], topics: list[tuple], num_assignments: int) -> list[tuple]:
    '''Generates random subscriber to topic assignments.
    Returns a list of tuples containing:
        - subscriber_topic_assignment_id
        - subscriber_id
        - topic_id
    '''
    assignments = []
    for i in range(1, num_assignments + 1):
        subscriber = random.choice(subscribers)
        topic = random.choice(topics)

        assignments.append((i, subscriber[0], topic[0]))
    return assignments


def generate_fake_articles(faker: Faker, num_articles: int, num_sources: int) -> list[tuple]:
    '''Generates fake article table entries.
    Returns a list of tuples containing:
        - article_id
        - article_title
        - polarity_score
        - source_id
        - date_published
        - article_url
    '''
    fake = Faker()
    articles = []
    source_polarity = [round(random.uniform(-1.0, 1.0), 2)
                       for _ in range(num_sources)]

    for i in range(1, num_articles + 1):
        article_id = i
        article_title = fake.sentence()
        source_id = random.randint(1, num_sources)

        polarity_score = random.triangular(source_polarity[source_id-1])

        date_published = fake.date_time_between(
            start_date='-5d', end_date='today')

        article_url = fake.url()

        articles.append((article_id, article_title, polarity_score,
                        source_id, date_published, article_url))

    return articles


if __name__ == "__main__":
    f = Faker()
    fake_subs = generate_fake_subscribers(f, 3)
    fake_topics = generate_fake_topics()
    fake_subs_topics = generate_fake_subscriber_topic_assignments(
        fake_subs, fake_topics, 12)
