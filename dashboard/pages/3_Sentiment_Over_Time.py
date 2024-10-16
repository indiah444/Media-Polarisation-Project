"""Script to create visualisations of changes over time"""
import streamlit as st
import altair as alt
import pandas as pd
from db_functions import get_scores_topic, get_topic_names
from d_graphs import visualise_change_over_time

AGGREGATES = ["mean", "count"]
WEEKDAY_ORDER = ['Monday', 'Tuesday', 'Wednesday',
                 'Thursday', 'Friday', 'Saturday', 'Sunday']


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


def construct_streamlit_time_graph(data: pd.DataFrame, avg_col, count_col, sent_by_title: bool, sampling: str):
    """Constructs a streamlit time graph."""

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


def add_year_month_day_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Adds year, week, and weekday columns to a dataframe"""
    data["year"] = data["date_published"].dt.year

    data["week_num"] = data["date_published"].dt.isocalendar().week

    data["month_name"] = data["date_published"].dt.strftime('%b')

    data["week_of_month"] = data["date_published"].apply(
        lambda d: (d.day - 1) // 7 + 1)

    data["week_text"] = data["month_name"] + \
        " Week " + data["week_of_month"].astype(str)

    data["weekday"] = data["date_published"].dt.day_name()
    data["date_name"] = data["date_published"].dt.strftime('%d-%m-%Y')
    return data


def construct_streamlit_heatmap(heatmaps_container, data: pd.DataFrame, by_title: bool, colourscheme: str = 'yellowgreen'):
    """Constructs a Streamlit heatmap with week_text on the x-axis but sorted by week_num"""
    vals = "title_polarity_score" if by_title else "content_polarity_score"
    data = data[["week_num", "weekday", vals, "week_text", "date_name"]]

    data = data.groupby(["week_num", "week_text", "weekday", "date_name"],
                        as_index=False)[vals].mean()

    heatmap = alt.Chart(data).mark_rect().encode(
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

        st.markdown("""This page shows trends in **compound** sentiment scores over time.
                The 'granularity' may be altered to smooth out the data: 
                at the lower end, sentiment scores are averaged over time periods of an hour, 
                and this can be increased up to 100 hours.""")

        sampling_rate = str(selected_frequency) + 'h'

        line_graphs = st.container()
        line_graphs.header(f"Polarity by Article Titles")
        col1, col2 = line_graphs.columns(2)

        construct_streamlit_time_graph(data,
                                       col1, col2,
                                       sent_by_title=True,
                                       sampling=sampling_rate)

        line_graphs.header(f"Polarity by Article Content")
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
