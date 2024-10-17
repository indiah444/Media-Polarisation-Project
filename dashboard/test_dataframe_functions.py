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
