# pylint: disable=C0103, E0401

"""A page with some graphs comparing all topics."""

import streamlit as st

from db_functions import get_avg_polarity_all_topics
from d_graphs import create_sentiment_distribution_chart, generate_html

if __name__ == "__main__":

    st.set_page_config(
        page_icon="📰",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("Welcome to the Media Polarisation Dashboard")

    st.markdown("""
    ## Overview of Media Polarisation

    Welcome to the <span style='color:blue; font-weight:bold;'>Overview</span> page of the Media Polarisation Dashboard. 
    Here, we provide insights into the <span style='color:red; font-weight:bold;'>sentiment scores</span> associated with various topics covered by different media outlets.

    This page will help you understand how different sources report on specific topics and the overall <span style='color:blue; font-weight:bold;'>sentiment</span> associated with these reports. 
    Use the graphs below to explore the data visually.
    """, unsafe_allow_html=True)

    data = get_avg_polarity_all_topics()
    if not data.empty:
        st.subheader(
            "Sentiment Distribution Graph")
        distribution_chart = create_sentiment_distribution_chart(data)
        st.altair_chart(distribution_chart, use_container_width=True)
        st.subheader(
            "Average Content Polarity Score by Topic and Source")
        st.html(generate_html(data))
    else:
        st.write("No data for the last week.")
