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
    ## 📊 Understanding Polarised Media Coverage and Sentiment
                
    In today's highly polarised media landscape, news outlets often present different
    narratives on the same event, making it challenging to assess the neutrality
    of the information you consume.
                
    Our <span style='color:red; font-weight:bold;'>**Media Polarisation Dashboard**</span> is designed to help you navigate this
    ever-changing terrain by providing insights into how different media sources
    from across the political spectrum cover key topics. 
                
    Through this dashboard, you can:
    - Compare <span style='color:blue; font-weight:bold;'>**topic coverage**</span> between various news outlets.
    - Analyse the <span style='color:red; font-weight:bold;'>**sentiment**</span> of articles from different sources.
    - Understand <span style='color:blue; font-weight:bold;'>**how frequently**</span> topics are covered and observe <span style='color:red; font-weight:bold;'>**shifts over time**</span>.
    - Visualise differences in <span style='color:blue; font-weight:bold;'>**media framing**</span>, empowering you to make more informed decisions about the information you trust.
                
    ## 🔍 How It Works
                
    This dashboard aggregates data from a range of news outlets, analysing articles for both <span style='color:red; font-weight:bold;'>**sentiment**</span> and <span style='color:blue; font-weight:bold;'>**frequency of coverage**</span>.
    We perform hourly updates using RSS feeds from these sources, and the data is then processed to determine how positively or negatively each topic is discussed.
    Additionally, you can <span style='color:red; font-weight:bold;'>**subscribe**</span> to daily or weekly email updates, ensuring you stay informed on how the media landscape evolves.
                
    ## 🚀 Explore the Data
                
    Use the tabs on the sidebar to begin exploring the data:
    - <span style='color:red; font-weight:bold;'>**Subscribe**</span>: The sign-up page for email updates. You can update your details, or unsubscribe from email updates if you wish from here.
    - <span style='color:blue; font-weight:bold;'>**Topic Filter**</span>: See how different outlets cover the same topics.
    - <span style='color:red; font-weight:bold;'>**Word Clouds**</span>: See a quick snapshot of the most common words used by different outlets.
                
    Our goal is to provide you a clearer picture of how sentiment and emotions shape media, giving you the tools to become a more critical news consumer.
    """, unsafe_allow_html=True)
