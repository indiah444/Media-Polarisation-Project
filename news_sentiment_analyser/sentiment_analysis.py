'''Methods for analysing sentiment of content.'''

import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime

nltk.download('vader_lexicon')


def get_sentiments(sia, df: pd.DataFrame, text_col: str, topic_col: str, source_col: str) -> pd.DataFrame:
    """Get sentiment data for a given text column.
    Returns a dataframe containing:
    text column, topic column and sentiments (pos,neg,neut,compound)."""

    if not pd.api.types.is_string_dtype(df[text_col]):
        raise TypeError("The text column must contain strings.")

    sents = df[text_col].apply(lambda x: sia.polarity_scores(x))

    sentiments = df.copy()

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
    sentiment_analyser = SentimentIntensityAnalyzer()
    fake_data = {
        "title": [
            "Trump Criticizes 2024 Election Process",
            "Harris Advocates for Climate Change Action",
            "Natural Disaster Strikes Coastal City",
            "Supreme Court Rules on Abortion Laws"
        ],
        "content": [
            "In a recent rally, Donald Trump h...",
            "Vice President Kamala Harris urged the...",
            "A devastating hurricane hit the...",
            "The Supreme Court ruled on..."
        ],
        "source_name": ["Fox News", "Democracy Now!", "Democracy Now!", "Fox News"],
        "published": [
            datetime(2023, 8, 12),
            datetime(2024, 3, 5),
            datetime(2024, 1, 22),
            datetime(2023, 10, 14)
        ],
        "link": [
            "https://example.com/trump-2024-criticism",
            "https://example.com/harris-climate-change",
            "https://example.com/natural-disaster-coast",
            "https://example.com/supreme-court-abortion"
        ],
        "topics": [
            ['Donald Trump', '2024 Presidential Election'],
            ['Kamala Harris', 'Climate Change'],
            ['Natural Disaster'],
            ['Abortion', 'Crime and Law Enforcement']
        ]
    }
    fake_articles = pd.DataFrame(fake_data)
    print(get_sentiments(sentiment_analyser,
          fake_articles, 'content', 'topics', 'source_name'))
