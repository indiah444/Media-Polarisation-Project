"""Script to create visualisations of changes over time"""

from datetime import datetime
import streamlit as st
import pandas as pd
import altair as alt
from db_functions import get_scores_topic


def resample_dataframe(df: pd.DataFrame, time_interval:str):
    """Resamples the dataframe to return the average sentiment scores by source, topic 
    over a set of grouped time intervals"""

    df['date_published'] =pd.to_datetime(df['date_published'])

    df_avg = df.groupby(['source_name', 'topic_name']).resample(time_interval, on= 'date_published').mean().reset_index()
    return df_avg

def generate_warning_message(source_to_topics: dict) -> str:
    """Generates a warning message that some sources don't cover some topics"""

    if not source_to_topics:
        return ""
    return "\n".join([
        f"""WARNING: {s} doesn't have any articles for {','.join(t)}"""
        for s, t in source_to_topics])


def visualise_change_over_time(df: pd.DataFrame, topic_name:str) -> alt.Chart:
    """Visualise changes in sentiment over time"""

    base = alt.Chart(df).encode(
    alt.Color("source_name",title='Source Name').legend(None)
    ).properties(
        width=500
    )
    line = base.mark_line().encode(
        x = alt.X('date_published:T', axis = alt.Axis(offset=-150,title = 'Date Published', titleAnchor="end")),
        y = alt.Y('title_polarity_score:Q',scale=alt.Scale(domain=[-1, 1]), title = 'Title Polarity Score')
    ).properties(
        width=500,
        title = f'Hourly Average of Sentiment Scores for a {topic_name}'
    )

    last_point = base.mark_circle(size=100, color='red').encode(
        x='date_published:T',
        y='title_polarity_score:Q'
    ).transform_window(
        rank='rank(date_published)',
        sort=[alt.SortField('date_published', order='descending')],
        groupby=['source_name']
    ).transform_filter(
        alt.datum.rank == 1
    )

    source_names = last_point.mark_text(align="left", dx=  10).encode(text="source_name")

    return  last_point + source_names + line

def construct_streamlit_time_graph():
    """Constructs a streamlit time graph"""

    topic_names = get_topic_names()
    st.sidebar.header("Topic")
    selected_topic = st.sidebar.selectbox("Choose a topic:", topic_names)
    selected_frequency = st.sidebar.slider(label="Number of hours to average over", min_value=1,max_value=24,step=1)
    sampling = str(selected_frequency) + 'h'
    if selected_topic:

        data = pd.DataFrame(get_scores_topic(selected_topic))
        if data.empty:
            st.text("No data to display.")
        else:
            averaged = resample_dataframe(data, sampling)
            averaged.dropna(inplace=True)
            line_graph = visualise_change_over_time(averaged, selected_topic)
            st.altair_chart(line_graph)

if __name__ == "__main__":
    construct_streamlit_time_graph()
