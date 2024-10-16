"""Script to find the topics of an article using openai."""

from os import environ as ENV
import json

from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
import pandas as pd

from database_functions import get_topic_names


def add_topics_to_dataframe(articles: pd.DataFrame) -> pd.DataFrame:
    """Returns the dataframe with a topics column added.
    Currently chuncking is set to 3 titles, but will be increased.
    May change title to article_title - check with others."""
    if 'title' not in articles.columns:
        raise ValueError("DataFrame must contain a 'title' column")
    if articles.empty:
        raise ValueError("DataFrame is empty")
    load_dotenv()
    ai = OpenAI(api_key=ENV["OPENAI_API_KEY"])
    titles = articles['title'].tolist()
    topic_test = get_topic_names()
    combined_topic_dict = {}
    for batch in chunk_list(titles, 15):
        batch_topic_dict = find_article_topics(batch, topic_test, ai)
        combined_topic_dict.update(batch_topic_dict)
    articles['topics'] = articles['title'].map(combined_topic_dict)
    df_filtered = articles[articles['topics'].apply(
        lambda x: isinstance(x, list) and len(x) > 0)]

    return df_filtered


def chunk_list(lst: list, chunk_size: int):
    """Chunks the list of titles into batches."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


def find_article_topics(article_titles: list[str], topics: list[str],
                        openai_client: OpenAI) -> dict:
    """Returns a dictionary of article title to topics associated with each article title."""
    titles = "\n".join(article_titles)
    system_content = create_message(topics)
    try:
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
    except OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return {title: [] for title in article_titles}
    except Exception as e:  # pylint: disable=W0718
        print(f"Unexpected error: {e}")
        return {title: [] for title in article_titles}
    try:
        raw_response = response.choices[0].message.content
        raw_response = raw_response.replace("'", '"')
        if raw_response.startswith("```json"):
            cleaned_response = raw_response.strip("```json").strip()
        else:
            cleaned_response = raw_response
        list_response = json.loads(cleaned_response)

    except (json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"Error processing API response: {e}")
        return {title: [] for title in article_titles}

    if isinstance(list_response, list):
        return {item['title']: item['topics'] for item in list_response}

    return {list_response['title']: list_response['topics']}


def create_message(topics: list[str]) -> str:
    """Creates the message to be sent to the openAI, as the system content."""
    content_topics = ", ".join(topics)
    message = f"""Your job is to return a object with the structure
    'title': title, 'topics': list of topics (or empty list if none),
    for each article title, in a list. The topics are: {content_topics}"""

    return message


if __name__ == "__main__":
    pass
