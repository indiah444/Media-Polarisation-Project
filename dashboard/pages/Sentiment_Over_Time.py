"""Script to create visualisations of changes over time"""

import streamlit as st
import pandas as pd
from db_functions import get_scores_topic, get_topic_names
from d_graphs import visualise_change_over_time


def resample_dataframe(df: pd.DataFrame, time_interval: str):
    """Resamples the dataframe to return the average sentiment scores by source, topic 
    over a set of grouped time intervals"""

    df['date_published'] = pd.to_datetime(df['date_published'])

    df_avg = df.groupby(['source_name', 'topic_name']).resample(
        time_interval, on='date_published').mean().reset_index()

    return df_avg


def generate_warning_message(source_to_topics: dict) -> str:
    """Generates a warning message that some sources don't cover some topics"""

    if not source_to_topics:
        return ""
    return "\n".join([
        f"""WARNING: {s} doesn't have any articles for {','.join(t)}"""
        for s, t in source_to_topics])


def construct_streamlit_time_graph(selected_topic: str, sent_by_title: bool):
    """Constructs a streamlit time graph"""

    if selected_topic:

        data = pd.DataFrame(get_scores_topic(selected_topic))

        if data.empty:
            st.text("No data to display.")
            return

        averaged = resample_dataframe(data, sampling).dropna()

        line_graph = visualise_change_over_time(
            averaged, by_title=sent_by_title)

        st.altair_chart(line_graph)


if __name__ == "__main__":
    st.title("Changes in Sentiment Over Time")
    topic_names = get_topic_names()
    st.sidebar.header("Topic")

    selected_topic = st.sidebar.selectbox("Choose a topic:", topic_names)

    selected_frequency = st.sidebar.slider(
        label="Granularity (hours)", min_value=1, max_value=100, step=1)

    sampling = str(selected_frequency) + 'h'

    st.title(f"Change in Sentiment of {selected_topic} Over Time")

    st.header(f"Polarity by Article Titles")

    construct_streamlit_time_graph(selected_topic, sent_by_title=True)

    st.header(f"Polarity by Article Content")
    construct_streamlit_time_graph(selected_topic, sent_by_title=False)
