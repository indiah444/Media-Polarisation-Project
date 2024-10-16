"""Script to transform the dataframe for inserting into RDS, adding topics, adding scores."""

import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from openai_topics import add_topics_to_dataframe
from database_functions import get_source_dict, get_article_titles
from sentiment_analysis import get_sentiments


def transform(articles: pd.DataFrame) -> pd.DataFrame:
    """Returns the transformed dataframe."""
    if articles.empty:
        return articles
    articles = drop_duplicate_titles(articles)
    if articles.empty:
        return articles
    articles = drop_already_present_articles(articles)
    if articles.empty:
        return articles
    articles = change_source_name_to_id(articles)
    articles = get_polarity_scores(articles)
    articles = add_topics_to_dataframe(articles)

    return articles


def change_source_name_to_id(articles: pd.DataFrame) -> pd.DataFrame:
    """Changes the source name to source_id for insertion into RDS."""
    source_id_dict = get_source_dict()
    articles['source_id'] = articles['source_name'].map(source_id_dict)
    articles = articles.drop(columns=['source_name'])

    return articles


def get_polarity_scores(articles: pd.DataFrame) -> pd.DataFrame:
    """Adds both title_polarity_score and content_polarity_score."""
    sentiment_analyser = SentimentIntensityAnalyzer()
    articles = get_title_polarity_score(articles, sentiment_analyser)
    articles = get_content_polarity_score(articles, sentiment_analyser)

    return articles


def get_title_polarity_score(articles: pd.DataFrame, sia) -> pd.DataFrame:
    """Adds a polarity score for the title."""
    articles = get_sentiments(sia, articles, 'title')
    articles = articles.drop(columns=['pos', 'neg', 'neut'])
    articles = articles.rename(columns={'compound': 'title_polarity_score'})
    return articles


def get_content_polarity_score(articles: pd.DataFrame, sia) -> pd.DataFrame:
    """Adds a polarity score for the content."""
    articles = get_sentiments(sia, articles, 'content')
    articles = articles.drop(columns=['pos', 'neg', 'neut'])
    articles = articles.rename(columns={'compound': 'content_polarity_score'})
    return articles


def drop_already_present_articles(articles: pd.DataFrame) -> pd.DataFrame:
    """Drops rows with titles already in the RDS."""
    article_titles = get_article_titles()
    articles = articles[~articles['title'].isin(article_titles)]

    return articles


def drop_duplicate_titles(articles: pd.DataFrame) -> pd.DataFrame:
    """Drops duplicate rows based on the 'title' column."""
    articles = articles.drop_duplicates(subset='title', keep='first')

    return articles


if __name__ == "__main__":
    pass
