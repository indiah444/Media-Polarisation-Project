# pylint: disable=C0103, E0401

"""A file to generate word clouds based on article word frequency by source."""

import re
from os import environ as ENV

import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer
from nltk import download as nltk_download
from psycopg2.extras import RealDictCursor
from psycopg2 import connect
from psycopg2.extensions import connection


def create_connection() -> connection:
    """Creates a connection to the RDS with postgres."""

    load_dotenv()
    conn = connect(dbname=ENV["DB_NAME"], user=ENV["DB_USER"],
                   host=ENV["DB_HOST"], password=ENV["DB_PASSWORD"],
                   port=ENV["DB_PORT"],
                   cursor_factory=RealDictCursor)

    return conn


@st.cache_data
def download_nltk_data():
    """Downloads the required NLTK data only once."""

    nltk_download("punkt")
    nltk_download("stopwords")
    nltk_download('punkt_tab')
    nltk_download("wordnet")


@st.cache_data
def get_all_article_content():
    """Returns all article content from the database."""

    with create_connection() as conn:
        query = """
        SELECT article_content, source_name
        FROM article
        JOIN source on article.source_id = source.source_id;
        """
        with conn.cursor() as cur:
            cur.execute(query)
            articles = cur.fetchall()

    fox_news_articles = [article["article_content"]
                         for article in articles if article["source_name"] == "Fox News"]
    democracy_now_articles = [article["article_content"]
                              for article in articles if article["source_name"] == "Democracy Now!"]

    return fox_news_articles, democracy_now_articles


W_TOKENIZER = WhitespaceTokenizer()
LEMMATIZER = WordNetLemmatizer()


def lemmatize_text(text: str) -> str:
    """Lemmatizes a given text, returning the lemmatized form of each word."""

    return ' '.join([LEMMATIZER.lemmatize(w) for w in W_TOKENIZER.tokenize(text)])


def clean_text(text: str, custom_stopwords: list) -> str:
    """Cleans text by removing URLs, punctuation, and stopwords."""

    stop_words = set(stopwords.words("english")) | set(custom_stopwords)

    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^\w\s]', '', text.lower())

    words = word_tokenize(text)
    words = [word for word in words if word not in stop_words and word.isalpha()]
    words = [word for word in words if len(word) > 2]

    lemmatized_words = lemmatize_text(' '.join(words))

    return lemmatized_words


@st.cache_data
def get_word_frequency(articles: list[str], custom_stopwords: list) -> dict:
    """Counts word frequencies in a given list of articles."""

    word_freq = {}

    for article in articles:
        cleaned_text = clean_text(article, custom_stopwords)
        words = cleaned_text.split()

        for word in words:
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1

    return word_freq


@st.cache_data
def generate_wordcloud(word_freq: dict, title: str, colormap: str):
    """Generates and returns a word cloud from word frequencies."""

    if not word_freq:
        st.warning(f"No words found to generate the word cloud for {title}.")
        return

    wordcloud = WordCloud(width=1000, height=500,
                          max_words=100, background_color="white",
                          colormap=colormap).generate_from_frequencies(word_freq)

    plt.figure(figsize=(10, 5), dpi=100)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(title, fontsize=20)
    st.pyplot(plt.gcf())


@st.cache_data
def run_app():
    """Runs the Word Cloud Streamlit page."""

    download_nltk_data()

    custom_stop_words = ["fox", "news", "said",
                         "get", "also", "would", "could", "click", "u"]

    st.title("Article Content Word Cloud by News Source")

    fn_articles, dn_articles = get_all_article_content()

    fox_news_word_freq = get_word_frequency(fn_articles, custom_stop_words)
    democracy_now_word_freq = get_word_frequency(
        dn_articles, custom_stop_words)

    st.header("Fox News Word Cloud")
    generate_wordcloud(fox_news_word_freq, "Fox News", colormap="Reds_r")

    st.header("Democracy Now! Word Cloud")
    generate_wordcloud(democracy_now_word_freq,
                       "Democracy Now!", colormap="PuBu")


if __name__ == "__main__":

    run_app()
