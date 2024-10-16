"""Script to create visualisations of changes over time"""
import streamlit as st
import altair as alt
import pandas as pd
from db_functions import get_scores_topic, get_topic_names
from d_graphs import visualise_change_over_time

AGGREGATES = ["mean", "count"]


@st.cache_data
def resample_dataframe(df: pd.DataFrame, time_interval: str, aggregate: str):
    """Resamples the dataframe to return the aggregate sentiment scores by 
    (source, topic) over a set of grouped time intervals."""

    if not aggregate in AGGREGATES:
        raise ValueError(
            f"The aggregate parameter must be one of {AGGREGATES}.")

    df['date_published'] = pd.to_datetime(df['date_published'])

    df_avg = df.groupby(['source_name', 'topic_name']).resample(
        time_interval, on='date_published').agg({"title_polarity_score": aggregate, "content_polarity_score": aggregate}).reset_index()

    return pd.DataFrame(df_avg)


def construct_streamlit_time_graph(data_df: pd.DataFrame, avg_col, count_col, sent_by_title: bool, sampling: str):
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


@st.cache_data
def add_year_month_day_columns(data_df: pd.DataFrame) -> pd.DataFrame:
    """Adds year, month, and weekday columns to a dataframe"""
    data_df["year"] = data_df["date_published"].dt.year
    data_df["month"] = data_df["date_published"].dt.month
    data_df["weekday"] = data_df["date_published"].dt.day_name()
    return data_df


def construct_streamlit_heatmap(heatmaps_container, data_df: pd.DataFrame, by_title: bool, colourscheme: str = 'blues'):
    """Constructs a streamlit heatmap"""

    vals = "title_polarity_score" if by_title else "content_polarity_score"

    data_df = data_df[["month", "weekday", vals]]
    data_df = data_df.groupby(["month", "weekday"], as_index=False)[
        vals].mean()

    heatmap = alt.Chart(data_df).mark_rect().encode(
        x=alt.X('month:O', title='Month'),
        y=alt.Y('weekday:O', title='Day of the Week'),
        color=alt.Color(f'{vals}:Q', title='Polarity Score',
                        scale=alt.Scale(scheme=colourscheme)),
        tooltip=[vals, 'month', 'weekday']
    ).properties(
        width=600,
        height=300
    )

    heatmaps_container.altair_chart(heatmap)


if __name__ == "__main__":

    topic_names = get_topic_names()

    st.sidebar.header("Settings")

    selected_topic = st.sidebar.selectbox("Choose a topic:", topic_names)
    data = pd.DataFrame(get_scores_topic(selected_topic))

    selected_frequency = st.sidebar.slider(
        label="Granularity (hours)", min_value=1, max_value=100, step=1)

    if data.empty:
        st.warning(f"No data available for {selected_topic}")

    else:
        data['date_published'] = pd.to_datetime(data['date_published'])
        st.title(f"Change in Sentiment of {selected_topic} Over Time")

        st.markdown("""This page shows trends in <span style='color:blue; font-weight:bold;'>**compound**</span> sentiment scores over time.
                The <span style='color:red;'>'granularity'</span> may be altered to smooth out the data: 
                at the lower end, sentiment scores are averaged over time periods of an hour, 
                and this can be increased up to 100 hours.""", unsafe_allow_html=True)

        sampling_rate = str(selected_frequency) + 'h'

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
        heatmaps.header("Heatmap of Polarity Scores")

        data = add_year_month_day_columns(data)

        years = data["year"].unique().tolist()
        sources = data["source_name"].unique().tolist() + ["All"]

        year = heatmaps.selectbox("Year:", years)
        source = heatmaps.selectbox("Source:", sources)

        data = data[data["year"] == year]

        if source != "All":
            data = data[data["source_name"] == source]

        heatmaps.subheader("By Title")
        construct_streamlit_heatmap(heatmaps, data, True)
        heatmaps.subheader("By Content")
        construct_streamlit_heatmap(heatmaps, data, False)
