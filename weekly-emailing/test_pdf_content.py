# pylint: skip-file

from io import BytesIO
from unittest.mock import patch

import pandas as pd

from pdf_content import generate_html_report, generate_pdf, add_source_columns, add_topic_rows


@patch('pdf_content.create_whisker_plot')
def test_generate_html_report(mock_create_whisker_plot, sample_data):

    mock_create_whisker_plot.return_value = 'base64_whisker_plot_image'
    html_content = generate_html_report(sample_data)

    assert isinstance(html_content, str)
    assert '<h1>Weekly Polarity Report</h1>' in html_content
    assert 'base64_whisker_plot_image' in html_content
    assert '<p>Data is based on articles published over the past week.</p>' in html_content


@patch('pdf_content.generate_html_report')
@patch('pdf_content.pisa.CreatePDF')
def test_generate_pdf(mock_create_pdf, mock_generate_html_report, sample_data):
    mock_generate_html_report.return_value = ''
    mock_create_pdf.return_value = None
    pdf_buffer = generate_pdf(sample_data)

    mock_generate_html_report.assert_called_once_with(sample_data)
    mock_create_pdf.assert_called_once()
    assert isinstance(pdf_buffer, BytesIO)


class TestAddSourceColumns:

    def test_with_valid_df(self):
        expected_data = {'source1': [0.3, 0.5], 'source2': [-0.2, -0.7]}
        df = pd.DataFrame(expected_data, index=['topic1', 'topic2'])
        df.index.name = 'topic_name'
        df.columns.name = 'source_name'
        result = add_source_columns(df)
        expected = "<th style='background-color: white;'>source1</th><th style='background-color: white;'>source2</th>"
        assert result == expected

    def test_empty_df(self):
        df = pd.DataFrame({})
        result = add_source_columns(df)
        expected = ""
        assert result == expected


class TestAddTopicRows:

    def test_add_topic_rows(self):
        data = {'source1': [0.3, 0.6],
                'source2': [-0.2, -0.7]}
        df = pd.DataFrame(data, index=['topic1', 'topic2'])
        result = add_topic_rows(df)
        expected = ("<tr><td style='background-color: white;'>topic1</td>"
                    "<td style='background-color: #fafafa;'>0.30</td>"
                    "<td style='background-color: #fafafa;'>-0.20</td></tr>"
                    "<tr><td style='background-color: white;'>topic2</td>"
                    "<td style='background-color: #b6f7ae;'>0.60</td>"
                    "<td style='background-color: #fabbb7;'>-0.70</td></tr>")
        assert result == expected

    def test_empty_df(self):
        df = pd.DataFrame({})
        result = add_topic_rows(df)
        expected = ""
        assert result == expected
