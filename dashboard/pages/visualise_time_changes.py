"""Script to create visualisations of changes over time"""

from datetime import datetime
import streamlit as st
import pandas as pd
import altair as alt
from db_functions import get_scores_topic, get_topic_names


def resample_dataframe(df: pd.DataFrame, time_interval: str, avg_over_source: bool):
    """Resamples the dataframe to return the average sentiment scores by source, topic 
    over a set of grouped time intervals"""

    df['date_published'] = pd.to_datetime(df['date_published'])

    if avg_over_source:
        df["source_name"] = "Average"
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


def get_last_point(df: pd.DataFrame) -> pd.DataFrame:
    """Returns a dataframe with the maximum date published for each source."""
    last_point_df = df.groupby('source_name').apply(
        lambda x: x.loc[x['date_published'].idxmax()]
    ).reset_index(drop=True)

    return last_point_df


def visualise_change_over_time(df: pd.DataFrame, by_title: bool) -> alt.Chart:
    """Visualise changes in sentiment over time"""

    base = alt.Chart(df).encode(
        alt.Color("source_name:N", title='Source Name').legend(None)
    ).properties(
        width=500
    ).interactive()

    if not by_title:
        y_axis = ('content_polarity_score', "Content Polarity Score")
    else:
        y_axis = ('title_polarity_score', "Title Polarity Score")

    line = base.mark_line().encode(
        x=alt.X('date_published:T', axis=alt.Axis(
            offset=-150, title='Date Published', titleAnchor="end")),
        y=alt.Y(f'{y_axis[0]}:Q', scale=alt.Scale(
            domain=[-1, 1]), title=y_axis[1]),
        tooltip=[alt.Tooltip(field="source_name", title="Source Name"),
                 alt.Tooltip(field=f"{y_axis[0]}",
                             title=f"Average {y_axis[1]}")]
    ).properties(
        width=500
    ).interactive()

    last_point = get_last_point(df)

    points = alt.Chart(last_point).mark_circle(size=100).encode(
        x='date_published:T',
        y=f'{y_axis[0]}:Q',
        tooltip=[alt.Tooltip('source_name:N', title='Source Name')],
        color=alt.Color('source_name:N')
    )

    source_names = points.mark_text(
        align="left", dx=10).encode(text="source_name")

    return points + source_names + line


def construct_streamlit_time_graph(selected_topic: str, sent_by_title: bool):
    """Constructs a streamlit time graph"""
    if selected_topic:

        data = pd.DataFrame(get_scores_topic(selected_topic))

        if data.empty:
            st.text("No data to display.")
        else:
            averaged = resample_dataframe(data, sampling, False).dropna()
            averaged_over_sources = resample_dataframe(
                data, sampling, True).dropna()

            line_graph = visualise_change_over_time(
                averaged, by_title=sent_by_title)

            if len(data["source_name"].unique()) > 1:
                avg_line = visualise_change_over_time(
                    averaged_over_sources, by_title=sent_by_title)
                st.altair_chart(line_graph + avg_line)
            else:
                st.altair_chart(line_graph)


if __name__ == "__main__":
    topic_names = get_topic_names()
    st.sidebar.header("Topic")

    selected_topic = st.sidebar.selectbox("Choose a topic:", topic_names)

    selected_frequency = st.sidebar.slider(
        label="Number of hours to average over", min_value=1, max_value=24, step=1)

    sampling = str(selected_frequency) + 'h'
    st.title(f"Change in Sentiment of {selected_topic} Over Time")
    st.header(f"Polarity by Article Titles")
    construct_streamlit_time_graph(selected_topic, sent_by_title=True)
    st.header(f"Polarity by Article Content")
    construct_streamlit_time_graph(selected_topic, sent_by_title=False)
