# pylint: disable=C0103, E0401, R0801

"""Script to create visualisations of changes over time"""

import streamlit as st
from streamlit.delta_generator import DeltaGenerator
import pandas as pd

from db_functions import get_scores_topic, get_topic_names
from d_graphs import visualise_change_over_time, visualise_heatmap
from dataframe_functions import resample_dataframe, add_year_month_day_columns
from streamlit_components import (construct_heatmaps_container, construct_linegraphs_container,
                                  add_settings_to_heatmaps_container, construct_sidebar)


def select_data_by_topic(topic_name: str) -> pd.DataFrame:
    """Selects the data for a topic by name"""
    score_data = get_scores_topic(topic_name)
    return pd.DataFrame(score_data)


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


def construct_streamlit_heatmap(heatmaps_container: DeltaGenerator,
                                weekly_data: pd.DataFrame, sent_by_title: bool,
                                colour: str = 'yellowgreen'):
    """Constructs a Streamlit heatmap with week_text on the x-axis but sorted by week_num"""
    header_text = "By Article Title" if sent_by_title else "By Article Content"
    heatmaps_container.subheader(header_text)
    heatmap = visualise_heatmap(weekly_data, sent_by_title, colour)
    heatmaps_container.altair_chart(heatmap, use_container_width=True)


if __name__ == "__main__":

    st.set_page_config(
        page_icon="📰",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    topic_names = get_topic_names()
    selected_topic, sampling_rate = construct_sidebar(topic_names)

    data = select_data_by_topic(selected_topic)

    if data.empty:
        st.warning(f"No data available for {selected_topic}")

    else:
        data['date_published'] = pd.to_datetime(data['date_published'])
        st.title(f"Change in Sentiment of {selected_topic} Over Time")

        st.html("""
                This page shows trends in 
                <span style='color:blue; font-weight:bold;'>compound</span> sentiment scores over time.
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

        content_avg, content_count = line_graph_cols[1]
        construct_streamlit_time_graph(data,
                                       content_avg,
                                       content_count,
                                       sent_by_title=False,
                                       sampling=sampling_rate)

        data = add_year_month_day_columns(data)

        heatmaps = construct_heatmaps_container()

        years = data["year"].unique().tolist()
        sources = data["source_name"].unique().tolist()

        year, source = add_settings_to_heatmaps_container(
            heatmaps, years, sources)

        data = data[data["year"] == year]

        if source != "All":
            data = data[data["source_name"] == source]

        construct_streamlit_heatmap(heatmaps, data, True)
        construct_streamlit_heatmap(heatmaps, data, False)
