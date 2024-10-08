'''Generates dummy data'''
from faker import Faker

TOPICS = []


def generate_fake_subscribers(fake: Faker, num: int) -> list[tuple]:
    '''Generates fake subscribers. 
    Returns a list of tuples containing:
        - subscriber_id
        - subscriber_email
        - subscriber_first_name
        - subscriber_surname  
    '''

    subscribers = []

    for i in range(num):
        sub_id = i
        email = fake.unique.email()
        first_name = fake.first_name()
        last_name = fake.last_name()
        subscribers.append((sub_id, email, first_name, last_name))
    return subscribers


if __name__ == "__main__":
    f = Faker()
    print(generate_fake_subscribers(f, 3))
