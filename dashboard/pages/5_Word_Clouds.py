# pylint: disable=C0103, E0401, R0801

"""A file to generate word clouds based on article word frequency by source."""

import re
from os import environ as ENV
from datetime import datetime, timedelta

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
import pandas as pd


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
    """Returns all article content from the database, along with their
    topics."""

    with create_connection() as conn:
        query = """
        SELECT article.article_id, article.article_content, source.source_name, article.date_published, 
               topic.topic_name
        FROM article
        JOIN source ON article.source_id = source.source_id
        LEFT JOIN article_topic_assignment ON article.article_id = article_topic_assignment.article_id
        LEFT JOIN topic ON article_topic_assignment.topic_id = topic.topic_id;
        """
        with conn.cursor() as cur:
            cur.execute(query)
            articles = cur.fetchall()

    return articles


def get_unique_topics():
    """Fetches unique topics from the database."""

    with create_connection() as conn:
        query = "SELECT topic_name FROM topic;"
        with conn.cursor() as cur:
            cur.execute(query)
            topics = cur.fetchall()

    return [topic["topic_name"] for topic in topics]


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


def filter_articles_by_date(articles: list, time_range: str):
    """Filters the articles based on the selected time range."""

    now = datetime.now()

    if time_range == 0:
        cutoff_date = now - timedelta(hours=1)
    elif time_range == 1:
        cutoff_date = now - timedelta(days=1)
    elif time_range == 2:
        cutoff_date = now - timedelta(days=7)
    else:
        return articles

    filtered_articles = [
        article for article in articles if article["date_published"] > cutoff_date.date()]

    return filtered_articles


def get_articles_by_source(filtered_articles: list, source_name: str) -> list:
    """Returns article contents for a given source from the filtered articles."""

    return [
        article for article in filtered_articles if article["source_name"] == source_name
    ]


@st.cache_data
def get_word_frequency(articles: list[str], custom_stopwords: list) -> dict:
    """Counts word frequencies in a given list of articles."""

    word_freq = {}

    for article in articles:
        cleaned_text = clean_text(article["article_content"], custom_stopwords)
        words = cleaned_text.split()

        for word in words:
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1

    return word_freq


def get_word_frequency_by_date(articles: list[dict], custom_stopwords: list) -> dict:
    """Counts word frequencies in a given list of articles, grouped by date."""

    word_freq_by_date = {}

    for article in articles:
        cleaned_text = clean_text(article["article_content"], custom_stopwords)
        words = cleaned_text.split()

        article_date = article["date_published"]
        if article_date not in word_freq_by_date:
            word_freq_by_date[article_date] = {}

        for word in words:
            if len(word) > 2:
                if word not in word_freq_by_date[article_date]:
                    word_freq_by_date[article_date][word] = 0

                word_freq_by_date[article_date][word] += 1

    return word_freq_by_date


def get_top_n_words_over_time(word_freq_by_date: dict, top_n: int) -> dict:
    """Gets the top N words over time period and their frequency by date."""

    cumulative_word_freq = {}

    for date, word_freq in word_freq_by_date.items():
        for word, freq in word_freq.items():
            if word not in cumulative_word_freq:
                cumulative_word_freq[word] = 0
            cumulative_word_freq[word] += freq

    top_n_words = sorted(cumulative_word_freq,
                         key=cumulative_word_freq.get, reverse=True)[:top_n]

    top_n_word_freq_over_time = {word: [] for word in top_n_words}

    for date in sorted(word_freq_by_date.keys()):
        word_freq_for_date = word_freq_by_date[date]
        for word in top_n_words:
            if word in word_freq_for_date:
                top_n_word_freq_over_time[word].append(
                    (date, word_freq_for_date[word]))
            else:
                top_n_word_freq_over_time[word].append((date, 0))

    return top_n_word_freq_over_time


def plot_bar_chart(word_freq_df: pd.DataFrame, title: str):
    """Plots a bar chart of word frequencies over time using Matplotlib."""

    # Set the DataFrame index to date for easier plotting
    word_freq_df = word_freq_df.sort_values('date')
    word_freq_df['date'] = pd.to_datetime(word_freq_df['date'])

    # Get the top 10 words
    # Unique words in the DataFrame
    top_words = word_freq_df['word'].unique()[:10]

    # Set up the bar chart
    plt.figure(figsize=(12, 6))

    for word in top_words:
        word_data = word_freq_df[word_freq_df['word'] == word]
        plt.bar(word_data['date'], word_data['frequency'], label=word)

    plt.title(f"Top Word Frequencies Over Time - {title}", fontsize=16)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(title="Words", loc="upper left", bbox_to_anchor=(1, 1))

    st.pyplot(plt.gcf())


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


def run_app():
    """Runs the Word Cloud Streamlit page."""

    download_nltk_data()

    custom_stop_words = ["fox", "news", "said",
                         "get", "also", "would", "could", "click", "u"]

    st.title("Article Content Word Cloud by News Source")

    time_range_options = ["Last hour", "Last 24 hours", "Last 7 days"]
    selected_time_range = st.sidebar.select_slider(
        "Select time range",
        options=time_range_options,
        value="Last 24 hours"
    )

    time_range_mapping = {
        "Last hour": 0,
        "Last 24 hours": 1,
        "Last 7 days": 2
    }
    time_range = time_range_mapping[selected_time_range]

    st.write(f"Time Range Selected: {selected_time_range}")

    unique_topics = get_unique_topics()
    selected_topics = st.sidebar.multiselect(
        "Select topics", options=unique_topics)

    articles = get_all_article_content()
    filtered_articles = filter_articles_by_date(articles, time_range)

    if selected_topics:
        filtered_articles = [
            article for article in filtered_articles if article["topic_name"] in selected_topics
        ]

    fn_articles = get_articles_by_source(filtered_articles, "Fox News")
    fn_word_freq_by_date = get_word_frequency_by_date(
        fn_articles, custom_stop_words)
    top_n_fn_words = get_top_n_words_over_time(fn_word_freq_by_date, top_n=10)

    fn_word_freq_data = []
    for word, freq_data in top_n_fn_words.items():
        for date, freq in freq_data:
            fn_word_freq_data.append(
                {'word': word, 'date': date, 'frequency': freq})

    fn_word_freq_df = pd.DataFrame(fn_word_freq_data)

    dn_articles = get_articles_by_source(filtered_articles, "Democracy Now!")
    dn_word_freq_by_date = get_word_frequency_by_date(
        dn_articles, custom_stop_words)
    top_n_dn_words = get_top_n_words_over_time(dn_word_freq_by_date, top_n=10)

    dn_word_freq_data = []
    for word, freq_data in top_n_dn_words.items():
        for date, freq in freq_data:
            dn_word_freq_data.append(
                {'word': word, 'date': date, 'frequency': freq})

    dn_word_freq_df = pd.DataFrame(dn_word_freq_data)

    fox_news_word_freq = get_word_frequency(fn_articles, custom_stop_words)
    democracy_now_word_freq = get_word_frequency(
        dn_articles, custom_stop_words)

    st.header("Fox News Word Cloud")
    generate_wordcloud(fox_news_word_freq, "Fox News", colormap="Reds_r")
    st.subheader("Fox News Top Word Trends")
    plot_bar_chart(fn_word_freq_df, "Fox News")

    st.header("Democracy Now! Word Cloud")
    generate_wordcloud(democracy_now_word_freq,
                       "Democracy Now!", colormap="PuBu")
    st.subheader("Democracy Now! Top Word Trends")
    plot_bar_chart(dn_word_freq_df, "Democracy Now!")


if __name__ == "__main__":

    run_app()
