from openai import OpenAI
from dotenv import load_dotenv
from os import environ as ENV
import json


def find_article_topics(article_titles: list[str], topics: list[str], openai_client) -> list[str]:
    """Returns a list of topics associated with the article title, using openAI."""
    content_topics = ", ".join(topics)
    titles = "\n".join(article_titles)
    system_content = f"Your job is to return a JSON object with the structure 'title': title, 'topics': list of topics (or empty list if none), for each article title. The topics are: {content_topics}"
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
    return response.choices[0].message.content


def create_message(article_title: str, topics: list[str]) -> str:
    """Creates the message to be sent to the openAI."""
    message_topics = "\n".join(topics)
    message = f"""Given the news title: '{article_title}', 
    identify which of the following topics it relates to:
    \n\n{message_topics} \n\n
    Please provide a list of matching topics in the format: 
    'title: topic1, topic2'. or just 'title' if there are no matching topics."""

    return message


def get_topics_from_response(response: str) -> list[str]:
    """Returns the formatted list of topics from the openai response."""
    if ":" not in response:
        return []


if __name__ == "__main__":
    load_dotenv()
    ai = OpenAI(api_key=ENV["OPENAI_API_KEY"])
    results = find_article_topics(['AI is on the rise', 'Travelling to Columbia', 'Plane flights to the world cup'],
                                  ['Travel', 'Technology', 'Sports Events'], ai)
    print(results)
    print(type(results))
    test = json.loads(results)
    print(test)
