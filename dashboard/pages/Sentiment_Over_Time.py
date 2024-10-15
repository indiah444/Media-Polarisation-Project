"""Script to create visualisations of changes over time"""
import streamlit as st
import altair as alt
import pandas as pd
from db_functions import get_scores_topic, get_topic_names
from d_graphs import visualise_change_over_time

AGGREGATES = ["mean", "count"]


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


def construct_streamlit_time_graph(avg_col, count_col, selected_topic: str, sent_by_title: bool):
    """Constructs a streamlit time graph."""
    if selected_topic:

        data = pd.DataFrame(get_scores_topic(selected_topic))

        averaged = resample_dataframe(data, sampling, "mean").dropna()

        counts = resample_dataframe(data, sampling, "count").dropna()

        avg_graph = visualise_change_over_time(
            averaged, by_title=sent_by_title)

        count_graph = visualise_change_over_time(
            counts, by_title=sent_by_title)

        avg_col.subheader(f"Average")
        avg_col.altair_chart(avg_graph, use_container_width=True)

        count_col.subheader(f"Count")
        count_col.altair_chart(count_graph, use_container_width=True)


def construct_streamlit_heatmap(container, selected_topic: str, by_title: bool, colourscheme: str = "yellowgreen"):
    """Constructs a streamlit heatmap"""
    data = pd.DataFrame(get_scores_topic(selected_topic))

    data['date_published'] = pd.to_datetime(data['date_published'])

    data["year"] = data["date_published"].dt.year
    data["month"] = data["date_published"].dt.month
    data["weekday"] = data["date_published"].dt.day_name()

    years = data["year"].unique().tolist()
    sources = data["source_name"].unique().tolist() + ["All"]

    year = container.selectbox("Year:", years)
    source = container.selectbox("Source:", sources)

    vals = "title_polarity_score" if by_title else "content_polarity_score"
    data = data[data["year"] == year]
    if source != "All":
        data = data[data["source_name"] == source]

    if data.empty:
        st.warning("No data to display.")
        return

    data = data[["month", "weekday", vals]]

    pivoted_data = pd.pivot_table(data,
                                  values=vals, index=['weekday'],
                                  columns=['month'], aggfunc='mean')

    heatmap = alt.Chart(data).mark_rect().encode(
        x=alt.X('month:O', title='Month'),
        y=alt.Y('weekday:O', title='Day of the Week'),
        color=alt.Color(f'{vals}:Q', title='Polarity Score',
                        scale=alt.Scale(scheme=colourscheme)),
        tooltip=[vals, 'month', 'weekday']
    ).properties(
        width=600,
        height=300
    )

    container.altair_chart(heatmap, use_container_width=True)


if __name__ == "__main__":

    topic_names = get_topic_names()

    st.sidebar.header("Topic")

    selected_topic = st.sidebar.selectbox("Choose a topic:", topic_names)
    st.title(f"Change in Sentiment of {selected_topic} Over Time")
    st.markdown("""This page shows trends in **compound** sentiment scores over time.
                The 'granularity' may be altered to smooth out the data: 
                at the lower end, sentiment scores are averaged over time periods of an hour, 
                and this can be increased up to 100 hours.""")

    selected_frequency = st.sidebar.slider(
        label="Granularity (hours)", min_value=1, max_value=100, step=1)

    sampling = str(selected_frequency) + 'h'

    st.header(f"Polarity by Article Titles")
    col1, col2 = st.columns(2)

    construct_streamlit_time_graph(
        col1, col2, selected_topic, sent_by_title=True)

    st.header(f"Polarity by Article Content")
    col3, col4 = st.columns(2)
    construct_streamlit_time_graph(
        col3, col4, selected_topic, sent_by_title=False)
    cont = st.container()
    cont.header("Heatmap of Polarity Scores")
    cont.subheader("Polarity by title")

    # construct_streamlit_heatmap(cont, selected_topic, True)
