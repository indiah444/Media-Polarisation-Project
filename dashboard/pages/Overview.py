"""A page with some graphs comparing all topics."""

import streamlit as st

from db_functions import get_avg_polarity_last_week
from d_graphs import create_bar_graph_of_topic_sentiment, create_sentiment_distribution_chart

if __name__ == "__main__":

    st.title("Some graphs comparing all sources.")
    data = get_avg_polarity_last_week()
    if not data.empty:
        st.subheader("Average Polarity Scores by Topic and Source")
        sentiment_bar_chart = create_bar_graph_of_topic_sentiment(data)
        st.altair_chart(sentiment_bar_chart, use_container_width=True)
        st.subheader("Sentiment Distribution Graph")
        distribution_chart = create_sentiment_distribution_chart(data)
        st.altair_chart(distribution_chart, use_container_width=True)
    else:
        st.write("No data for the last week.")
