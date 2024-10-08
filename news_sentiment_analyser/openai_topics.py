"""Script to find the topics of an article using openai."""
from os import environ as ENV
import json

from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd

from database_functions import get_topic_names


def add_topics_to_dataframe(articles: pd.DataFrame) -> pd.DataFrame:
    """Returns the dataframe with a topics column added."""


def find_article_topics(article_titles: list[str], topics: list[str], openai_client) -> list[str]:
    """Returns a list of topics associated with each article title, using openAI."""
    titles = "\n".join(article_titles)
    system_content = create_message(topics)
    response = openai_client.chat.completions.create(
        messages=[

            {
                "role": "system",
                "content": system_content
            },
            {
                "role": "user",
                "content": titles,
            }],
        model="gpt-4o-mini",
    )
    response = json.loads(response.choices[0].message.content)
    return response


def create_message(topics: list[str]) -> str:
    """Creates the message to be sent to the openAI, as the system content."""
    content_topics = ", ".join(topics)
    message = f"""Your job is to return a JSON object with the structure 
    'title': title, 'topics': list of topics (or empty list if none), 
    for each article title. The topics are: {content_topics}"""

    return message


if __name__ == "__main__":
    load_dotenv()
    ai = OpenAI(api_key=ENV["OPENAI_API_KEY"])
    results = find_article_topics(['AI is on the rise', 'Travelling to Columbia', 'Plane flights to the world cup'],
                                  ['Travel', 'Technology', 'Sports Events'], ai)
    print(results[0])
