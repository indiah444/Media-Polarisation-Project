"""A file for cleaning article data by removing stopwords, unwanted
characters, whitespace etc."""

import re

import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")


def remove_urls(text: str) -> str:
    """Removes URLs from text."""

    return re.sub(r'http\S+', '', text)


def clean_multiple_spaces(text: str) -> str:
    """Returns text multiple spaces removed."""

    cleaned_text = re.sub(r'\s+', ' ', text)
    return cleaned_text.strip()


def remove_stopwords(text: str) -> str:
    """Removes stopwords from text."""

    stopwords_set = set(stopwords.words("english"))
    words = text.lower().split()
    words = [word.strip() for word in words if word not in stopwords_set]

    return ' '.join(words)


def clean_text(text: str) -> str:
    """Cleans the article text by applying all the cleaning steps."""

    text = remove_urls(text)
    text = clean_multiple_spaces(text)
    text = remove_stopwords(text)

    return text


if __name__ == "__main__":

    example_article_content = "Arizona began early voting Wednesday, marking yet another major swing state where voting is underway in the 2024 election. With Arizona now in the mix, 41 states and Washington, D.C., have launched some form of early voting https://www.foxnews.com/politics/days-until-voting-starts-election-season-kicks-off-sooner"
    cleaned_example_text = clean_text(example_article_content)

    print(f"Original text: {example_article_content}")
    print(f"Cleaned text: {cleaned_example_text}")
