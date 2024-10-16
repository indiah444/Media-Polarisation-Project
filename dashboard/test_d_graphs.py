# pylint skip-file
"""Testing the d_graphs file"""
import re
import pytest
from unittest.mock import patch
import pandas as pd
import datetime
from d_graphs import pivot_df, get_last_point, generate_html, add_source_columns


def add_source_columns(df: pd.DataFrame) -> str:
    """Add the source names as column titles."""
    color_scheme = {'Fox News': 'red', 'Democracy Now!': 'blue'}
    html = ""
    for source in df.columns:
        html += ("<th style='background-color: white; color:"
                 f"{color_scheme[source]};'>{source}</th>")
    return html


def test_add_source_cols():
    df = pd.DataFrame(columns={'Fox News': [], 'Democracy Now!': []})
    color_scheme = {'Fox News': 'red', 'Democracy Now!': 'blue'}
    assert add_source_columns(
        df) == "<th style='background-color: white; color:red;'>Fox News</th>" + "<th style='background-color: white; color:blue;'>Democracy Now!</th>"


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


@patch('d_graphs.add_topic_rows')
@patch('d_graphs.add_source_columns')
@patch('d_graphs.pivot_df')
def test_generate_html(mock_pivot_df, mock_add_source_columns, mock_add_topic_rows):
    mock_pivot_df.return_value = pd.DataFrame({
        'sourceA': [0.5],
        'sourceB': [0.6]
    }, index=['topic1'])

    mock_add_source_columns.return_value = "<th>Source A</th><th>Source B</th>"
    mock_add_topic_rows.return_value = "<tr><td>topic1</td><td>0.5</td><td>0.6</td></tr>"

    df = pd.DataFrame({
        'topic_name': ['topic1', "topic1"],
        'source_name': ['sourceA', 'sourceB'],
        'avg_polarity_score': [0.5, 0.6]
    })

    expected_html = """
    <html>
    <head>
        <style>
            table {
                font-family: Arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
        <table>
            <thead>
                <tr>
                    <th style='background-color: white; color: black'>Topic</th>
                    <th>Source A</th><th>Source B</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>topic1</td><td>0.5</td><td>0.6</td></tr>
            </tbody>
        </table>
    </body>
    </html>
    """
    result = generate_html(df)
    assert re.sub(r'\s+', ' ', result).strip() == re.sub(r'\s+',
                                                         ' ', expected_html).strip()


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
