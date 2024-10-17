"""Write unit tests for dataframe functions"""
import pytest
from unittest.mock import patch

import pandas as pd

from dataframe_functions import resample_dataframe, is_valid_time_interval


@patch("dataframe_functions.AGGREGATES", return_value=["mean", "count"])
def test_resample_dataframes_fails_with_invalid_aggregate(mock_aggregates):
    """Tests that resample dataframe fails with an invalid aggregate argument"""
    df = pd.DataFrame([])
    with pytest.raises(ValueError):
        resample_dataframe(df, '1h', 'invalid')


@pytest.mark.parametrize("interval", [
    ("5h"),
    ("12h"),
    ("0h"),
])
def test_is_valid_time_interval_valid(interval):
    """No exception should be raised for valid intervals"""
    assert is_valid_time_interval(interval) is None


@pytest.mark.parametrize("interval", [
    ("5m"),
    ("abc"),
    ("123"),
    ("h"),
    (""),
    (" 5h"),
    ("5 h"),
])
def test_is_valid_time_interval_invalid(interval):
    """Check if the appropriate error is raised for invalid intervals"""
    with pytest.raises(ValueError):
        is_valid_time_interval(interval)


def test_resample_dataframe_valid():
    """Asserts that resample dataframe is valid for resampling over an hour"""
    data = {
        "source_name": ["Source1", "Source1", "Source2", "Source2"],
        "topic_name": ["Topic1", "Topic1", "Topic2", "Topic2"],
        "date_published": pd.to_datetime(["2024-10-01 10:00", "2024-10-01 11:00", "2024-10-02 12:00", "2024-10-02 13:00"]),
        "title_polarity_score": [0.1, 0.2, 0.3, 0.4],
        "content_polarity_score": [0.5, 0.6, 0.7, 0.8]
    }
    df = pd.DataFrame(data)

    result_df = resample_dataframe(df, "1h", "mean")

    pd.testing.assert_frame_equal(result_df, result_df)


def test_resample_dataframe_24h():
    """Asserts that resample dataframe is valid for resampling over 24 hours"""
    data = {
        "source_name": ["Source1", "Source1", "Source2", "Source2"],
        "topic_name": ["Topic1", "Topic1", "Topic2", "Topic2"],
        "date_published": pd.to_datetime([
            "2024-10-01 10:00",
            "2024-10-01 11:00",
            "2024-10-02 12:00",
            "2024-10-02 13:00"
        ]),
        "title_polarity_score": [0.1, 0.2, 0.3, 0.4],
        "content_polarity_score": [0.5, 0.6, 0.7, 0.8]
    }
    df = pd.DataFrame(data)

    result_df = resample_dataframe(df, "24h", "mean")

    expected_data = {
        "source_name": ["Source1", "Source2"],
        "topic_name": ["Topic1", "Topic2"],
        "date_published": pd.to_datetime([
            "2024-10-01",  # Aggregated over the first day for Source1
            "2024-10-02"   # Aggregated over the second day for Source2
        ]),
        # Averaged for each day and source/topic
        "title_polarity_score": [0.15, 0.35],
        "content_polarity_score": [0.55, 0.75]
    }
    expected_df = pd.DataFrame(expected_data)

    pd.testing.assert_frame_equal(result_df, expected_df)
