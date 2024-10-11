import re

import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

from db_functions import create_connection

load_dotenv()

nltk.download("punkt")
nltk.download("stopwords")


def get_all_article_content():
    """Returns all article content from the database."""

    with create_connection() as conn:
        query = "SELECT article_content FROM article;"
        with conn.cursor() as cur:
            cur.execute(query)
            articles = cur.fetchall()

    return [article["article_content"] for article in articles]


def clean_text(text: str) -> str:
    """Cleans text by removing URLs, punctuation, and stopwords."""

    stop_words = set(stopwords.words("english"))

    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^\w\s]', '', text.lower())

    words = word_tokenize(text)
    words = [word for word in words if word not in stop_words and word.isalpha()]

    return ' '.join(words)


def get_word_frequency(articles: list[str]) -> dict:
    """Counts word frequencies in a given list of articles."""

    word_freq = {}

    for article in articles:
        cleaned_text = clean_text(article)
        words = cleaned_text.split()

        for word in words:
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1

    return word_freq


def generate_wordcloud(word_freq: dict):
    """Generates and returns a word cloud from word frequencies."""

    wordcloud = WordCloud(
        width=800, height=400, background_color="white").generate_from_frequencies(word_freq)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

    st.pyplot(plt)


st.title("Article Content Word Cloud")

articles = get_all_article_content()
word_freq = get_word_frequency(articles)

generate_wordcloud(word_freq)
