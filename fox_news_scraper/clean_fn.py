"""A file for cleaning article data by removing stopwords, unwanted
characters, whitespace etc."""

import re
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")
STOPWORDS = set(stopwords.words("english"))


def clean_text(text: str) -> str:
    """Cleans the article text by removing unwanted characters, stopwords etc."""

    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^\w\s]', '', text)

    words = text.lower().split()
    words = [word for word in words if word not in STOPWORDS]

    cleaned_text = ' '.join(words)
    return cleaned_text


if __name__ == "__main__":

    example_article_content = "Arizona began early voting Wednesday, marking yet another major swing state where voting is underway in the 2024 election. With Arizona now in the mix, 41 states and Washington, D.C., have launched some form of early voting https://www.foxnews.com/politics/days-until-voting-starts-election-season-kicks-off-sooner"
    cleaned_example_text = clean_text(example_article_content)

    print(f"Original text: {example_article_content}")
    print(f"Cleaned text: {cleaned_example_text}")
