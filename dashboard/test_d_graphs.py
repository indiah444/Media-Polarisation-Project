# pylint skip-file
"""Testing the d_graphs file"""
import pytest
import pandas as pd
import datetime
from d_graphs import pivot_df, get_last_point


@pytest.fixture
def example_df():
    """Returns an example dataframe"""
    return pd.DataFrame(
        [
            {'topic_name': 'Donald Trump',
             'source_name': 'Fox News',
             'content_polarity_score': 0.0,
             'title_polarity_score': -0.3712,
             'date_published': datetime.date(2024, 10, 10)},
            {'topic_name': 'Donald Trump',
             'source_name': 'Fox News',
             'content_polarity_score': -0.9781,
             'title_polarity_score': -0.3612,
             'date_published': datetime.date(2024, 10, 9)}

        ])


def test_pivot_df():
    data = {
        'topic_name': ['topic1', 'topic1', 'topic2', 'topic2'],
        'source_name': ['sourceA', 'sourceB', 'sourceA', 'sourceB'],
        'avg_polarity_score': [0.5, 0.6, 0.1, 0.3]
    }
    df = pd.DataFrame(data)
    expected_output = pd.DataFrame({
        'sourceA': [0.5, 0.1],
        'sourceB': [0.6, 0.3]
    }, index=['topic1', 'topic2']).fillna('N/A')
    expected_output.index.name = "topic_name"
    expected_output.columns.name = "source_name"
    result = pivot_df(df)
    pd.testing.assert_frame_equal(result, expected_output)


def test_pivot_df_with_empty_values():
    data = {
        'topic_name': ['topic1', 'topic2', 'topic2'],
        'source_name': ['sourceA', 'sourceA', 'sourceB'],
        'avg_polarity_score': [0.5, None, 0.3]
    }
    df = pd.DataFrame(data)
    expected_output = pd.DataFrame({
        'sourceA': [0.5, 'N/A'],
        'sourceB': ['N/A', 0.3]
    }, index=['topic1', 'topic2']).fillna('N/A')
    expected_output.index.name = "topic_name"
    expected_output.columns.name = "source_name"
    result = pivot_df(df)
    pd.testing.assert_frame_equal(result, expected_output)
