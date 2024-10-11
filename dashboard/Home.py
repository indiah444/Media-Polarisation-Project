"""Our main home page - that would appear when you click on the link!"""

import streamlit as st

if __name__ == "__main__":

    st.set_page_config(
        page_title="Media Polarisation Dashboard",
        page_icon="📰",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("Welcome to the Media Polarisation Dashboard")
    st.markdown("""
    ## Understanding Polarised Media Coverage and Sentiment
                
    In today's highly polarised media landscape, news outlets often present different
    narratives on the same event, making it challenging to assess the neutrality
    of the information you consume.
                
    Our **Media Polarisation Dashboard** is designed to help you navigate this
    ever-changing terrain by providing insights into how different media sources
    from across the political spectrum cover key topics.
                
    Through this dashboard, you can:
    - Compare **topic coverage** between various news outlets.
    - Analyse the **sentiment** of articles from different sources.
    - Understand **how frequently** topics are covered and observe **shifts over time**.
    - Visualise differences in **media framing**, empowering you to make more informed decisions about the information you trust.
                
    ## How It Works
                
    This dashboard aggregates data from a range of news outlets, analysing articles for both **sentiment** and **frequency of coverage**.
    We perform hourly updates using RSS feeds from these sources, and the data is then processed to determine how positively or negatively each topic is discussed.
    Additionally, you can **subscribe** to daily or weekly email updates, ensuring you stay informed on how the media landscape evolves over time.
                
    ## Explore the Data
                
    Use the tabs on the side bar to begin exploring the data:
    - **Subscribe**: The sign-up page for email updates. You can update your details, or unsubscribe from email updates if you wish from here.
    - **Topic Filter**: See jpw different outlets cover the same topics.
    - **Word Clouds**: See a quick snapshot of the most common words used by different outlets.
                
    Our goal is to provide you with a clearer picture of how sentiment and emotions shape media, giving you the tools to become a more critical consumer of news.
    """)
