"""Script to find the topics of an article using openai."""
from os import environ as ENV
import json

from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd

from database_functions import get_topic_names


def add_topics_to_dataframe(articles: pd.DataFrame) -> pd.DataFrame:
    """Returns the dataframe with a topics column added."""
    load_dotenv()
    ai = OpenAI(api_key=ENV["OPENAI_API_KEY"])
    titles = articles['title'].tolist()
    topic_test = get_topic_names()
    combined_dict = {}
    for batch in chunk_list(titles, 3):
        batch_result = find_article_topics(batch, topic_test, ai)
        combined_dict.update(batch_result)
    articles['topics'] = articles['title'].map(combined_dict)
    df_filtered = articles[articles['topics'].apply(
        lambda x: len(x) > 0)]

    return df_filtered


def chunk_list(lst, chunk_size):
    """Chunks the list of titles into batches."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


def find_article_topics(article_titles: list[str], topics: list[str], openai_client: OpenAI) -> str:
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
    raw_response = response.choices[0].message.content
    raw_response = raw_response.replace("'", '"')
    list_response = json.loads(raw_response)
    return {item['title']: item['topics'] for item in list_response}


def create_message(topics: list[str]) -> str:
    """Creates the message to be sent to the openAI, as the system content."""
    content_topics = ", ".join(topics)
    message = f"""Your job is to return a object with the structure 
    'title': title, 'topics': list of topics (or empty list if none), 
    for each article title, in a list. The topics are: {content_topics}"""

    return message


if __name__ == "__main__":
    data = {
        'title': [
            "AI Breakthrough in Healthcare",
            "Climate Change Impacts on Agriculture",
            "New Discoveries in Quantum Computing",
            "The Rise of Electric Vehicles",
            "Space Exploration: Next Frontier"
        ],
        'description': [
            "A recent breakthrough in AI applications promises to revolutionize the healthcare industry by improving diagnostic accuracy and personalized treatments.",
            "Studies reveal the growing impact of climate change on global agriculture, with challenges in food security and crop yields.",
            "Quantum computing is set to transform industries as new discoveries make it more feasible for solving complex problems at unprecedented speeds.",
            "Electric vehicles are experiencing a global rise in popularity, driven by advancements in battery technology and environmental concerns.",
            "As space agencies and private companies ramp up efforts, the next frontier in space exploration could bring new opportunities and challenges."
        ]
    }

# Create DataFrame
    df_articles = pd.DataFrame(data)
    result = add_topics_to_dataframe(df_articles)
    print(result)
