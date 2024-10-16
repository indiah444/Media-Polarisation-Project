# pylint skip-file
"""Testing the d_graphs file"""
import re
import altair as alt
import pytest
from unittest.mock import patch
import pandas as pd
import datetime
from d_graphs import pivot_df, get_last_point, generate_html, add_source_columns, create_bubble_chart


@pytest.fixture
def data():
    return {
        'source_name': ['Fox News', 'Democracy Now!', 'Fox News'],
        'avg_polarity_score': [0.2, 0.5, -0.1],
        'article_count': [100, 150, 80]
    }


def test_create_bubble_chart_creates_chart(data):
    df = pd.DataFrame(data)
    chart = create_bubble_chart(df)
    assert isinstance(
        chart, alt.Chart)


def test_bubble_chart_size(data):
    df = pd.DataFrame(data)
    chart = create_bubble_chart(df)
    assert chart.width == 800
    assert chart.height == 400


def test_get_last_point():
    data = {
        'source_name': ['sourceA', 'sourceA', 'sourceB'],
        'topic_name': ['topic1', 'topic2',  'topic2'],
        'date_published': ['2024-10-14', '2024-10-15', '2024-10-13'],
        'title_polarity_score': [0.5, 0.6,  0.8],
        'content_polarity_score': [0.3, 0.4,  0.7]
    }

    df = pd.DataFrame(data)
    df['date_published'] = pd.to_datetime(
        df['date_published'], errors='coerce')

    expected_data = {
        'source_name': ['sourceA', 'sourceB'],
        'topic_name': ['topic2', 'topic2'],
        'date_published': [pd.Timestamp('2024-10-15'), pd.Timestamp('2024-10-13')],
        'title_polarity_score': [0.6, 0.8],
        'content_polarity_score': [0.4, 0.7]
    }

    expected_df = pd.DataFrame(expected_data)

    result_df = get_last_point(df)

    pd.testing.assert_frame_equal(result_df, expected_df)


def test_add_source_cols():
    df = pd.DataFrame(columns={'Fox News': [], 'Democracy Now!': []})
    assert add_source_columns(
        df) == "<th style='background-color: white; color:red;'>Fox News</th>" + "<th style='background-color: white; color:blue;'>Democracy Now!</th>"


def test_add_source_cols_one_col():
    df = pd.DataFrame(columns={'Fox News': []})
    assert add_source_columns(
        df) == "<th style='background-color: white; color:red;'>Fox News</th>"


def test_add_source_cols_not_recognised():
    df = pd.DataFrame(columns={'Fox': []})
    with pytest.raises(KeyError):
        add_source_columns(df)


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
