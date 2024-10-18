# pylint: disable=C0103, E0401

"""One page showing a few graphs, where you can filter by topic."""

import streamlit as st

from db_functions import (get_topic_names, get_topic_dict,
                          get_average_score_per_source_for_a_topic,
                          get_title_and_content_data_for_a_topic)
from d_graphs import create_bubble_chart, create_scatter_graph

if __name__ == "__main__":

    st.set_page_config(
        page_icon="📰",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("Topic-Based Polarity Analysis with Altair")

    st.sidebar.header("Select Topic")
    topic_names = get_topic_names()
    topic_dict = get_topic_dict()
    selected_topic = st.sidebar.selectbox("Choose a topic:", topic_names)

    st.subheader(
        f"Bubble Chart: Average Polarity by Source (Topic: {selected_topic})")

    if selected_topic:
        topic_id = topic_dict[selected_topic]
        bubble_data = get_average_score_per_source_for_a_topic(topic_id)

        if not bubble_data.empty:

            bubble_chart = create_bubble_chart(bubble_data)

            st.altair_chart(bubble_chart, use_container_width=True)
        else:
            st.write("No data available for the selected topic in the last week.")

    st.subheader(
        f"Scatter Plot: Title vs Content Polarity (Topic: {selected_topic})")

    if selected_topic:
        scatter_data = get_title_and_content_data_for_a_topic(topic_id)

        if not scatter_data.empty:

            scatter_chart = create_scatter_graph(scatter_data)

            st.altair_chart(scatter_chart, use_container_width=True)
        else:
            st.write("No articles found for the selected topic in the last week.")
