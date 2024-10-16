"""Our main home page - that would appear when you click on the link!"""

import streamlit as st

if __name__ == "__main__":

    st.set_page_config(
        page_title="Media Polarisation Dashboard",
        page_icon="📰",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    BLUE = '#4ea8de'
    RED = '#ff6f61'

    # pylint: disable=C0103
    st.title("Welcome to the Media Polarisation Dashboard")
    st.markdown(f"""
    ## 📊 Understanding Polarised Media Coverage and Sentiment

    In today's highly polarised media landscape, news outlets often present different
    narratives on the same event, making it challenging to assess the neutrality
    of the information you consume.

    Our <span style='color:{RED}; font-weight:bold;'>**Media Polarisation Dashboard**</span> is designed to help you navigate this
    ever-changing terrain by providing insights into how different media sources
    from across the political spectrum cover key topics.

    Through this dashboard, you can:
    - Compare <span style='color:{BLUE}; font-weight:bold;'>**topic coverage**</span> between various news outlets.
    - Analyse the <span style='color:{RED}; font-weight:bold;'>**sentiment**</span> of articles from different sources.
    - Understand <span style='color:{BLUE}; font-weight:bold;'>**how frequently**</span> topics are coveRED and observe <span style='color:{RED}; font-weight:bold;'>**shifts over time**</span>.
    - Visualise differences in <span style='color:{BLUE}; font-weight:bold;'>**media framing**</span>, empowering you to make more informed decisions about the information you trust.

    ## 🔍 How It Works

    This dashboard aggregates data from a range of news outlets, analysing articles for both <span style='color:{RED}; font-weight:bold;'>**sentiment**</span> and <span style='color:{BLUE}; font-weight:bold;'>**frequency of coverage**</span>.
    We perform hourly updates using RSS feeds from these sources, and the data is then processed to determine how positively or negatively each topic is discussed.
    Additionally, you can <span style='color:{RED}; font-weight:bold;'>**subscribe**</span> to daily or weekly email updates, ensuring you stay informed on how the media landscape evolves.

    ## 🚀 Explore the Data

    Use the tabs on the sidebar to begin exploring the data:
    - <a href="http://ec2-35-179-130-166.eu-west-2.compute.amazonaws.com:8501/Overview" style='color:{RED}; font-weight:bold;'>**Overview**</a>: Get a broad understanding of media polarisation, including key visualisations that summarise the sentiment and coverage across different outlets.
    - <a href="http://ec2-35-179-130-166.eu-west-2.compute.amazonaws.com:8501/Sentiment_Over_Time" style='color:{BLUE}; font-weight:bold;'>**Sentiment Over Time**</a>: See how sentiment has shifted over time for various topics. This page provides interactive charts to help you visualise trends in media coverage.
    - <a href="http://ec2-35-179-130-166.eu-west-2.compute.amazonaws.com:8501/Topic_Filter" style='color:{RED}; font-weight:bold;'>**Topic Filter**</a>: Dive deep into specific topics and compare how different outlets cover them. You can filter by topics to see the varying sentiments used.
    - <a href="http://ec2-35-179-130-166.eu-west-2.compute.amazonaws.com:8501/Word_Clouds" style='color:{BLUE}; font-weight:bold;'>**Word Clouds**</a>: Visualise the most frequently used words by different media outlets. This page provides quick insights into the language and framing used in coverage.
    - <a href="http://ec2-35-179-130-166.eu-west-2.compute.amazonaws.com:8501/Subscribe" style='color:{RED}; font-weight:bold;'>**Subscribe**</a>: Sign up for daily or weekly email updates. You can manage your subscription preferences and ensure you stay informed about new insights and changes in media coverage.

    Our goal is to provide you a clearer picture of how sentiment and emotions shape media, giving you the tools to become a more critical news consumer.
    """, unsafe_allow_html=True)
