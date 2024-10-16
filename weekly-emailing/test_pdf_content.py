# pylint: skip-file

from io import BytesIO
from unittest.mock import patch

from pdf_content import generate_html_report, generate_pdf


@patch('pdf_content.create_bar_graph')
@patch('pdf_content.create_sentiment_distribution_chart')
def test_generate_html_report(mock_create_sentiment_chart, mock_create_bar_graph, sample_data):

    mock_create_bar_graph.return_value = 'base64_bar_graph_image'
    mock_create_sentiment_chart.return_value = 'base64_sentiment_chart_image'
    html_content = generate_html_report(sample_data)

    assert isinstance(html_content, str)
    assert '<h1>Weekly Polarity Report</h1>' in html_content
    assert 'base64_bar_graph_image' in html_content
    assert 'base64_sentiment_chart_image' in html_content
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
