'''Methods for analysing sentiment of content.'''

import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')


def get_sentiments(sia, df: pd.DataFrame, text_col: str, topic_col: str, source_col: str) -> pd.DataFrame:
    """Get sentiment data for a given text column.
    Returns a dataframe containing:
    text column, topic column and sentiments (pos,neg,neut,compound)."""

    if df[text_col].dtype == 'object':
        raise TypeError("The text column must contain strings.")

    sents = df[text_col].apply(lambda x: sia.polarity_scores(x))

    sentiments = df[[text_col, topic_col, source_col]]

    sentiments["pos"] = sents.apply(lambda x: x['pos'])
    sentiments["neg"] = sents.apply(lambda x: x['neg'])
    sentiments["neut"] = sents.apply(lambda x: x['neu'])
    sentiments["compound"] = sents.apply(lambda x: x['compound'])

    return sentiments


def get_avg_sentiment(sentiments: pd.DataFrame, topic_col: str, source_col: str) -> pd.DataFrame:
    """Returns the average sentiment for unique topics and sources"""

    return sentiments.groupby([topic_col, source_col]).agg({
        'pos': 'mean',
        'neg': 'mean',
        'neut': 'mean',
        'compound': 'mean'
    }).reset_index()


if __name__ == "__main__":
    sia = SentimentIntensityAnalyzer()
