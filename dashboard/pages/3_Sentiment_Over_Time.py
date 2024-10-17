# pylint: disable=C0103, E0401

"""Script to create visualisations of changes over time"""

import streamlit as st
from streamlit.delta_generator import DeltaGenerator
import altair as alt
import pandas as pd

from db_functions import get_scores_topic, get_topic_names
from d_graphs import visualise_change_over_time, visualise_heatmap

AGGREGATES = ["mean", "count"]


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


def select_data_by_topic(topic_name: str) -> pd.DataFrame:
    """Selects the data for a topic by name"""
    data = get_scores_topic(topic_name)
    return pd.DataFrame(data)


def construct_linegraphs_container() -> list[list]:
    """Constructs a container for the linegraphs on the streamlit page. 
    Returns the columns in the array arrangement they appear."""
    line_graphs = st.container()
    line_graphs.header("Polarity by Article Titles")
    avg_by_title, count_by_title = line_graphs.columns(2)
    line_graphs.header("Polarity by Article Content")
    avg_by_content, count_by_content = line_graphs.columns(2)
    line_graphs.header("Polarity by Article Content")
    return [[avg_by_title, count_by_title], [avg_by_content, count_by_content]]


def construct_heatmaps_container() -> DeltaGenerator:
    """Constructs a container for the heatmaps on the streamlit page.
    Returns the container."""
    heatmaps = st.container()
    heatmaps.header("Heatmap of Average Polarity Scores")
    return heatmaps


def add_settings_to_heatmaps_container(heatmaps_container: DeltaGenerator, 
                                       years_available: list[str],
                                       sources_available: list[str]):
    """Adds select boxes to heatmaps container.
    Returns the resulting (year,source)"""
    if not "All" in sources_available:
        sources_available += ["All"]
    year = heatmaps.selectbox("Year:", years_available)
    source = heatmaps.selectbox("Source:", sources_available)
    return year, source

if __name__ == "__main__":
    topic_names = get_topic_names()
    selected_topic, sampling_rate = construct_sidebar(topic_names)

    data = select_data_by_topic(selected_topic)

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
        
        line_graph_cols = construct_linegraphs_container()
        title_avg, title_count = line_graph_cols[0]
        construct_streamlit_time_graph(data,
                                       title_avg, 
                                       title_count,
                                       sent_by_title=True,
                                       sampling=sampling_rate)

        content_avg, content_count = line_graph_cols[0]
        construct_streamlit_time_graph(data,
                                       content_avg, 
                                       content_count,
                                       sent_by_title=False,
                                       sampling=sampling_rate)

    

        data = add_year_month_day_columns(data)

        heatmaps = construct_heatmaps_container()

        years = data["year"].unique().tolist()
        sources = data["source_name"].unique().tolist() + ["All"]

        year, source = add_settings_to_heatmaps_container(heatmaps, years, sources)

        data = data[data["year"] == year]

        if source != "All":
            data = data[data["source_name"] == source]

        construct_streamlit_heatmap(heatmaps, data, True)
        construct_streamlit_heatmap(heatmaps, data, False)
