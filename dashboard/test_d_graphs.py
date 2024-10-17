# pylint skip-file

"""Testing the d_graphs file"""

import re
import datetime
from unittest.mock import patch

import pytest
import pandas as pd
import altair as alt

from d_graphs import (pivot_df, get_last_point, generate_html, add_source_columns,
                      create_bubble_chart, create_scatter_graph, create_horizontal_line,
                      create_vertical_line, visualise_change_over_time)


class TestCreateBubbleChart:

    def test_creates_chart(self, fake_aggregated_data):
        df = pd.DataFrame(fake_aggregated_data)
        chart = create_bubble_chart(df)
        assert isinstance(chart, alt.Chart)

    def test_size(self, fake_aggregated_data):
        df = pd.DataFrame(fake_aggregated_data)
        chart = create_bubble_chart(df)
        assert chart.width == 800
        assert chart.height == 400


class TestCreateLines():

    def test_horizontal_line(self):
        line = create_horizontal_line()
        assert isinstance(line, alt.Chart)
        assert line.encoding['y'].shorthand == 'y:Q'

    def test_vertical_line(self):
        line = create_vertical_line()
        assert isinstance(line, alt.Chart)
        assert line.encoding['x'].shorthand == 'x:Q'


class TestCreateScatterGraph:

    @patch('d_graphs.create_vertical_line')
    @patch('d_graphs.create_horizontal_line')
    def test_creates_chart(self, mock_create_horizontal_line, mock_create_vertical_line, fake_aggregated_data):

        mock_create_horizontal_line.return_value = alt.Chart()
        mock_create_vertical_line.return_value = alt.Chart()

        df = pd.DataFrame(fake_aggregated_data)
        chart = create_scatter_graph(df)

        assert isinstance(chart, alt.LayerChart)
        assert len(chart.layer) == 3
        assert isinstance(chart.layer[0], alt.Chart)
        assert isinstance(chart.layer[1], alt.Chart)
        assert isinstance(chart.layer[2], alt.Chart)

    @patch('d_graphs.create_vertical_line')
    @patch('d_graphs.create_horizontal_line')
    def test_size(self, mock_create_horizontal_line, mock_create_vertical_line, fake_aggregated_data):
        df = pd.DataFrame(fake_aggregated_data)
        chart = create_scatter_graph(df)
        assert chart.width == 800
        assert chart.height == 400


class TestVisualiseChangeOverTime:

    def test_create_graph(self, fake_data):
        df = pd.DataFrame(fake_data)
        print(df)
        graph = visualise_change_over_time(df, True)
        assert isinstance(graph, alt.LayerChart)
        assert len(graph.layer) == 3
        assert isinstance(graph.layer[0], alt.Chart)
        assert isinstance(graph.layer[1], alt.Chart)
        assert isinstance(graph.layer[2], alt.Chart)

    def test_create_graph_by_title_true(self, fake_data):
        df = pd.DataFrame(fake_data)
        graph = visualise_change_over_time(df, True)
        assert isinstance(graph, alt.LayerChart)

    def test_create_graph_by_title_false(self, fake_data):
        df = pd.DataFrame(fake_data)
        graph = visualise_change_over_time(df, False)
        assert isinstance(graph, alt.LayerChart)


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
