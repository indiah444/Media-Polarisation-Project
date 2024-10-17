# pylint: skip-file

"""Tests for load_csv_fn"""

from datetime import datetime
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

from load_csv_fn import combine_entries_to_dataframe, process_rss_feeds_and_upload


@patch('load_csv_fn.upload_dataframe_to_s3')
@patch('load_csv_fn.combine_entries_to_dataframe')
@patch('load_csv_fn.fetch_from_multiple_feeds')
@patch('load_csv_fn.ENV', {'S3_BUCKET_NAME': 'test-bucket'})
@patch('load_csv_fn.datetime')
def test_process_rss_feeds_and_upload(mock_datetime, mock_fetch, mock_combine, mock_upload):
    """Mocks the test process RSS feed process"""
    mock_datetime.now.return_value.strftime.return_value = "2024-10-11_12-00-00"
    entries = {'col1': [1, 2], 'col2': [3, 4]}
    mock_fetch.return_value = entries
    mock_combine.return_value = pd.DataFrame(entries)

    feed_urls = ["http://example.com/feed1", "http://example.com/feed2"]

    process_rss_feeds_and_upload(feed_urls)

    mock_fetch.assert_called_once_with(feed_urls)

    mock_combine.assert_called_once_with(entries)

    args, kwargs = mock_upload.call_args
    pd.testing.assert_frame_equal(args[0],  pd.DataFrame(entries))
    assert args[1] == "test-bucket"
    assert args[2] == "2024-10-11_12-00-00_fox_news_article_data.csv"


@pytest.mark.parametrize("entries", [
    ([{'col1': [1, 2], 'col2': [3, 4]}]),
    ([{'col1': [1], 'col2': [3]}]),
    ([({'col1': [], 'col2': []})])
])
def test_combine_entries_into_df(entries):
    """Asserts that combine_entries_into_df returns the correct output"""
    expected_cols = entries[0].keys()
    assert set(combine_entries_to_dataframe(
        entries).columns) == set(expected_cols)
