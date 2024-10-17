# pylint: skip-file

"""Tests for pipeline_fn.py"""

from unittest.mock import patch

from pipeline_fn import lambda_handler

with patch('pipeline_fn.load_dotenv') as mock_load_dotenv:
    mock_load_dotenv.return_value = dict()


@patch('pipeline_fn.RSS_FEED_URLS')
@patch('pipeline_fn.process_rss_feeds_and_upload')
def test_lambda_handler_success_status(mock_process_rss, mock_rss_feed_urls):
    """Test lambda_handler success case."""

    mock_process_rss.return_value = None
    mock_rss_feed_urls.return_value = [
        "https://moxie.foxnews.com/google-publisher/latest.xml"]
    event = {}
    context = {}

    response = lambda_handler(event, context)

    assert response["statusCode"] == 200
    assert response["body"] == "RSS feed data processed and uploaded to S3 successfully."


@patch('pipeline_fn.RSS_FEED_URLS')
@patch('pipeline_fn.process_rss_feeds_and_upload')
def test_lambda_handler_process_called_correctly(mock_process_rss, mock_rss_feed_urls):
    """Test lambda_handler success case."""

    mock_process_rss.return_value = None

    mock_rss_feed_urls.return_value = [
        "https://moxie.foxnews.com/google-publisher/latest.xml"]

    event = {}
    context = {}

    lambda_handler(event, context)

    mock_process_rss.assert_called_once_with(mock_rss_feed_urls)


@patch('pipeline_fn.RSS_FEED_URLS')
@patch('pipeline_fn.process_rss_feeds_and_upload')
def test_lambda_handler_failure_status(mock_process_rss, mock_rss_feed_urls):
    """Test lambda_handler failure case."""

    mock_rss_feed_urls.return_value = [
        "https://moxie.foxnews.com/google-publisher/latest.xml"]

    mock_process_rss.side_effect = Exception()

    event = {}
    context = {}

    response = lambda_handler(event, context)

    assert response["statusCode"] == 500


@patch('pipeline_fn.RSS_FEED_URLS')
@patch('pipeline_fn.process_rss_feeds_and_upload')
def test_lambda_handler_failure_error_message(mock_process_rss, mock_rss_feed_urls):
    """Test lambda_handler failure case."""

    mock_rss_feed_urls.return_value = [
        "https://moxie.foxnews.com/google-publisher/latest.xml"]

    mock_process_rss.side_effect = Exception("S3 upload failed")

    event = {}
    context = {}

    response = lambda_handler(event, context)

    assert "Error: S3 upload failed" in response["body"]
