"""Methods for operating on pandas dataframes"""

import streamlit as st
import pandas as pd


AGGREGATES = ["mean", "count"]


def is_valid_time_interval(interval: str) -> None:
    """Raises an error if a time interval is invalid"""
    if not interval or not interval[-1] == "h":
        raise ValueError(
            "The time interval should represent a string in hours.")
    if not interval[:-1].isnumeric():
        raise ValueError(
            "The time interval should start with a number"
        )


@st.cache_data
def resample_dataframe(df: pd.DataFrame, time_interval: str, aggregate: str):
    """Resamples the dataframe to return the aggregate sentiment scores by 
    (source, topic) over a set of grouped time intervals."""

    if not aggregate in AGGREGATES:
        raise ValueError(
            f"The aggregate parameter must be one of {AGGREGATES}.")

    is_valid_time_interval(time_interval)

    df_avg = df.groupby(['source_name', 'topic_name']).resample(
        time_interval, on='date_published').agg({"title_polarity_score": aggregate,
                                                 "content_polarity_score": aggregate}).reset_index()

    return pd.DataFrame(df_avg)


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
