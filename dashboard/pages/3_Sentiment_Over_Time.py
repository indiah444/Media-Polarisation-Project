# pylint: disable=C0103, E0401

"""Script to create visualisations of changes over time"""

import streamlit as st
from streamlit.delta_generator import DeltaGenerator
import altair as alt
import pandas as pd

from db_functions import get_scores_topic, get_topic_names
from d_graphs import visualise_change_over_time

AGGREGATES = ["mean", "count"]
WEEKDAY_ORDER = ['Monday', 'Tuesday', 'Wednesday',
                 'Thursday', 'Friday', 'Saturday', 'Sunday']


@st.cache_data
def resample_dataframe(df: pd.DataFrame, time_interval: str, aggregate: str):
    """Resamples the dataframe to return the aggregate sentiment scores by 
    (source, topic) over a set of grouped time intervals."""
    if not aggregate in AGGREGATES:
        raise ValueError(
            f"The aggregate parameter must be one of {AGGREGATES}.")

    df_avg = df.groupby(['source_name', 'topic_name']).resample(
        time_interval, on='date_published').agg({"title_polarity_score": aggregate,
                                                 "content_polarity_score": aggregate}).reset_index()

    return pd.DataFrame(df_avg)


def construct_streamlit_time_graph(data_df: pd.DataFrame, avg_col: DeltaGenerator,
                                   count_col: DeltaGenerator, sent_by_title: bool, sampling: str):
    """Constructs a streamlit time graph."""
    averaged = resample_dataframe(data_df, sampling, "mean").dropna()

    counts = resample_dataframe(data_df, sampling, "count").dropna()

    avg_graph = visualise_change_over_time(
        averaged, by_title=sent_by_title)

    count_graph = visualise_change_over_time(
        counts, by_title=sent_by_title)

    avg_col.subheader("Average")
    avg_col.altair_chart(avg_graph, use_container_width=True)

    count_col.subheader("Count")
    count_col.altair_chart(count_graph, use_container_width=True)


def add_year_month_day_columns(data_df: pd.DataFrame) -> pd.DataFrame:
    """Adds year, week, and weekday columns to a dataframe"""
    data_df["year"] = data_df["date_published"].dt.year
    data_df["week_num"] = data_df["date_published"].dt.isocalendar().week
    data_df["month_name"] = data_df["date_published"].dt.strftime('%b')
    data_df["week_of_month"] = data_df["date_published"].apply(
        lambda d: (d.day - 1) // 7 + 1)
    data_df["week_text"] = data_df["month_name"] + \
        " Week " + data_df["week_of_month"].astype(str)
    data_df["weekday"] = data_df["date_published"].dt.day_name()
    data_df["date_name"] = data_df["date_published"].dt.strftime('%d-%m-%Y')
    return data_df


def visualise_heatmap(data_df: pd.DataFrame, by_title: bool, colourscheme: str = 'yellowgreen') -> alt.Chart:
    """Returns an altair heatmap"""
    vals = "title_polarity_score" if by_title else "content_polarity_score"
    data_df = data_df[["week_num", "weekday", vals, "week_text", "date_name"]]

    data_df = data_df.groupby(["week_num", "week_text", "weekday", "date_name"],
                              as_index=False)[vals].mean()

    return alt.Chart(data_df).mark_rect().encode(
        x=alt.X('week_text:O', title='Week', sort=alt.EncodingSortField(
            field='week_num', order='ascending')),
        y=alt.Y('weekday:O', title='Day of the Week',  sort=WEEKDAY_ORDER),
        color=alt.Color(f'{vals}:Q', title='Polarity Score',
                        scale=alt.Scale(scheme=colourscheme)),
        tooltip=[vals, 'date_name', 'weekday']
    ).properties(
        width=600,
        height=300
    )


def construct_streamlit_heatmap(heatmaps_container: DeltaGenerator,
                                weekly_data: pd.DataFrame, sent_by_title: bool,
                                colour: str = 'yellowgreen'):
    """Constructs a Streamlit heatmap with week_text on the x-axis but sorted by week_num"""
    header_text = "By Article Title" if sent_by_title else "By Article Content"
    heatmaps_container.subheader(header_text)
    heatmap = visualise_heatmap(weekly_data, sent_by_title, colour)
    heatmaps_container.altair_chart(heatmap)


def construct_sidebar(topics_list: list[str]) -> tuple[str, str]:
    """Constructs the Sidebar for the streamlit page.
    Returns (topic, granularity)"""
    st.sidebar.header("Settings")
    topic = st.sidebar.selectbox("Topic", topics_list)
    granularity_to_hours = {"1 hour": "1h",
                            "1 day": "24h", "1 week": str(24*7)+'h'}
    granularity = st.sidebar.selectbox(
        "Granularity", granularity_to_hours.keys())
    return topic, granularity_to_hours[granularity]


if __name__ == "__main__":
    topic_names = get_topic_names()
    selected_topic, sampling_rate = construct_sidebar(topic_names)
    data = pd.DataFrame(get_scores_topic(selected_topic))

    if data.empty:
        st.warning(f"No data available for {selected_topic}")

    else:
        data['date_published'] = pd.to_datetime(data['date_published'])
        st.title(f"Change in Sentiment of {selected_topic} Over Time")

        st.html("""
                This page shows trends in <span style='color:blue; font-weight:bold;'>compound</span> sentiment scores over time.
                The <span style='color:red;'>granularity</span> may be altered to smooth out the data: 

                at the lower end, sentiment scores are averaged over time buckets of an hour, and this can 
                be increased up to a day.
                """)

        line_graphs = st.container()
        line_graphs.header("Polarity by Article Titles")
        col1, col2 = line_graphs.columns(2)

        construct_streamlit_time_graph(data,
                                       col1, col2,
                                       sent_by_title=True,
                                       sampling=sampling_rate)

        line_graphs.header("Polarity by Article Content")
        col3, col4 = line_graphs.columns(2)
        construct_streamlit_time_graph(data,
                                       col3, col4,
                                       sent_by_title=False,
                                       sampling=sampling_rate)

        heatmaps = st.container()
        heatmaps.header("Heatmap of Average Polarity Scores")

        data = add_year_month_day_columns(data)

        years = data["year"].unique().tolist()
        sources = data["source_name"].unique().tolist() + ["All"]

        year = heatmaps.selectbox("Year:", years)
        source = heatmaps.selectbox("Source:", sources)

        data = data[data["year"] == year]

        if source != "All":
            data = data[data["source_name"] == source]

        construct_streamlit_heatmap(heatmaps, data, True)
        construct_streamlit_heatmap(heatmaps, data, False)
