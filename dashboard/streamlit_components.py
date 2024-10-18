"""Functions for creating streamlit components"""
import streamlit as st
from streamlit.delta_generator import DeltaGenerator

GRANULARITY_TO_HOURS = {"1 hour": "1h",
                        "1 day": "24h", "1 week": str(24*7)+'h'}


def select_topic(topics_list: list[str]) -> str:
    """Returns the selected topic."""
    topic = st.sidebar.selectbox("Topic", topics_list)
    return topic


def select_granularity(granularity_to_hours: dict) -> str:
    """Returns the selected granularity as a formatted string."""
    granularity = st.sidebar.selectbox(
        "Granularity", granularity_to_hours.keys())
    return granularity_to_hours[granularity]


def construct_sidebar(topics_list: list[str]) -> tuple[str, str]:
    """Constructs the Sidebar for the streamlit page.
    Returns (topic, granularity)"""
    st.sidebar.header("Settings")
    selected_topic = select_topic(topics_list)
    selected_granularity = select_granularity(GRANULARITY_TO_HOURS)
    return selected_topic, selected_granularity


def construct_linegraphs_container() -> list[list]:
    """Constructs a container for the linegraphs on the 
    sentiment over time page. 
    Returns the columns in the array arrangement they appear."""
    line_graphs = st.container()
    line_graphs.header("Polarity by Article Titles")
    avg_by_title, count_by_title = line_graphs.columns(2)
    line_graphs.header("Polarity by Article Content")
    avg_by_content, count_by_content = line_graphs.columns(2)

    return [[avg_by_title, count_by_title], [avg_by_content, count_by_content]]


def construct_heatmaps_container() -> DeltaGenerator:
    """Constructs a container for the heatmaps on the on the 
    sentiment over time page. 
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
    year = heatmaps_container.selectbox("Year:", years_available)
    source = heatmaps_container.selectbox("Source:", sources_available)
    return year, source
