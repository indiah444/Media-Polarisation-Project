# pylint: skip-file

"""Testing the d_graphs file"""

import re
from unittest.mock import patch

import pytest
import pandas as pd
import altair as alt

from d_graphs import (pivot_df, get_last_point, generate_html, add_source_columns,
                      create_bubble_chart, create_scatter_graph, create_horizontal_line,
                      create_vertical_line, visualise_change_over_time,
                      create_sentiment_distribution_chart, visualise_heatmap, add_topic_rows)


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
        assert graph.layer[0].encoding.y['title'] == "Title Polarity Score"

    def test_create_graph_by_title_false(self, fake_data):
        df = pd.DataFrame(fake_data)
        graph = visualise_change_over_time(df, False)

        assert isinstance(graph, alt.LayerChart)
        assert graph.layer[0].encoding.y['title'] == "Content Polarity Score"


class TestCreateSentimentDistributionChart:

    @patch('d_graphs.create_vertical_line')
    def test_create_graph(self, mock_create_vertical_line, fake_data):
        mock_create_vertical_line.return_value = alt.Chart()

        df = pd.DataFrame(fake_data)
        graph = create_sentiment_distribution_chart(df)

        assert isinstance(graph, alt.LayerChart)
        assert len(graph.layer) == 2
        assert isinstance(graph.layer[0], alt.Chart)
        assert isinstance(graph.layer[1], alt.Chart)

    @patch('d_graphs.create_vertical_line')
    def test_size(self, mock_create_vertical_line, fake_data):
        mock_create_vertical_line.return_value = alt.Chart()

        df = pd.DataFrame(fake_data)
        graph = create_sentiment_distribution_chart(df)

        assert graph.width == 400
        assert graph.height == 300


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


class TestAddTopicRows:
    def test_with_sample_data(self, sample_df):
        expected_html = (
            "<tr><td style='background-color: white; color: black;'>Topic 1</td>"
            "<td style='background-color: #b6f7ae; color: black;'>0.70</td>"
            "<td style='background-color: #fabbb7; color: black;'>-0.80</td>"
            "</tr>"
            "<tr><td style='background-color: white; color: black;'>Topic 2</td>"
            "<td style='background-color: #fabbb7; color: black;'>-0.60</td>"
            "<td style='background-color: #fafafa; color: black;'>0.30</td>"
            "</tr>"
            "<tr><td style='background-color: white; color: black;'>Topic 3</td>"
            "<td style='background-color: white; color: black;'>N/A</td>"
            "<td style='background-color: white; color: black;'>N/A</td>"
            "</tr>"
        )

        result_html = add_topic_rows(sample_df)
        assert result_html == expected_html

    def test_with_empty_df(self):
        empty_df = pd.DataFrame()
        expected_html = ""
        result_html = add_topic_rows(empty_df)
        assert result_html == expected_html

    def test_with_non_float_values(self):
        df = pd.DataFrame(
            {'Fox News': ['N/A'], 'Democracy Now!': ['N/A']}, index=['Topic 1'])
        expected_html = (
            "<tr><td style='background-color: white; color: black;'>Topic 1</td>"
            "<td style='background-color: white; color: black;'>N/A</td>"
            "<td style='background-color: white; color: black;'>N/A</td>"
            "</tr>"
        )

        result_html = add_topic_rows(df)
        assert result_html == expected_html

    def test_with_positive_and_negative_scores(self):
        df = pd.DataFrame(
            {'Fox News': [0.6], 'Democracy Now!': [-0.7]}, index=['Topic 1'])
        expected_html = (
            "<tr><td style='background-color: white; color: black;'>Topic 1</td>"
            "<td style='background-color: #b6f7ae; color: black;'>0.60</td>"
            "<td style='background-color: #fabbb7; color: black;'>-0.70</td>"
            "</tr>"
        )

        result_html = add_topic_rows(df)
        assert result_html == expected_html


class TestPivotDf:

    def test_pivot(self):
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

    def test_pivot_with_none_values(self):
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

    def test_pivot_with_empty_df(self):
        data = {
            'topic_name': [],
            'source_name': [],
            'avg_polarity_score': []
        }
        df = pd.DataFrame(data)
        result = pivot_df(df)

        assert result.empty


class TestAddSourceCols:
    def test_add_source_cols(self):
        df = pd.DataFrame(columns={'Fox News': [], 'Democracy Now!': []})

        assert add_source_columns(df) == \
            "<th style='background-color: white; color:red;'>Fox News</th>" + \
            "<th style='background-color: white; color:blue;'>Democracy Now!</th>"

    def test_add_one_col(self):
        df = pd.DataFrame(columns={'Fox News': []})

        assert add_source_columns(df) == \
            "<th style='background-color: white; color:red;'>Fox News</th>"

    def test_add_cols_not_recognised(self):
        df = pd.DataFrame(columns={'Fox': []})

        with pytest.raises(KeyError):
            add_source_columns(df)


class TestGenerateHtml:

    def reformat_whitespace(self, string):
        return re.sub(r'\s+', ' ', string).strip()

    @patch('d_graphs.add_topic_rows')
    @patch('d_graphs.add_source_columns')
    @patch('d_graphs.pivot_df')
    def test_html_string(self, mock_pivot_df, mock_add_source_columns, mock_add_topic_rows):

        mock_pivot_df.return_value = {}
        mock_add_source_columns.return_value = "<th></th>"
        mock_add_topic_rows.return_value = "<tr></tr>"

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
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <tr></tr>
                </tbody>
            </table>
        </body>
        </html>
        """
        result = generate_html({})

        assert self.reformat_whitespace(
            result) == self.reformat_whitespace(expected_html)

    @pytest.mark.parametrize('input_td, input_th, func_input', [("<th>Source A</th><th>Source B</th>",
                                                                 "<tr><td>topic1</td><td>0.5</td><td>0.6</td></tr>", 1),
                                                                ("", "", 2),
                                                                ("Test", "Test", 3)])
    @patch('d_graphs.add_topic_rows')
    @patch('d_graphs.add_source_columns')
    @patch('d_graphs.pivot_df')
    def test_inputs(self, mock_pivot_df, mock_add_source_columns, mock_add_topic_rows, input_td, input_th, func_input):

        mock_pivot_df.return_value = {}
        mock_add_source_columns.return_value = input_td
        mock_add_topic_rows.return_value = input_th

        result = generate_html(func_input)

        expected_tr = f"""<tr>
                              <th style='background-color: white; color: black'>Topic</th>
                              {input_td}
                          </tr>"""

        expected_tbody = f"""<tbody>
                                {input_th}
                             </tbody>"""

        expected_tr = self.reformat_whitespace(expected_tr)
        expected_tbody = self.reformat_whitespace(expected_tbody)
        result = self.reformat_whitespace(result)

        assert expected_tr in result
        assert expected_tbody in result


class TestVisualiseHeatmap:

    def test_creation(self, fake_heatmap_data):
        df = pd.DataFrame(fake_heatmap_data)
        chart = visualise_heatmap(df, True)

        assert isinstance(chart, alt.Chart)

    def test_by_title_true(self, fake_heatmap_data):
        df = pd.DataFrame(fake_heatmap_data)
        chart = visualise_heatmap(df, True)

        assert chart.encoding.color['shorthand'].startswith(
            'title_polarity_score')

    def test_by_title_false(self, fake_heatmap_data):
        df = pd.DataFrame(fake_heatmap_data)
        chart = visualise_heatmap(df, False)

        assert chart.encoding.color['shorthand'].startswith(
            'content_polarity_score')

    def test_size(self, fake_heatmap_data):
        df = pd.DataFrame(fake_heatmap_data)
        chart = visualise_heatmap(df, True)

        assert chart.width == 600
        assert chart.height == 300
