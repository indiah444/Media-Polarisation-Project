"""Test file for functions in extract_fn.py"""

from unittest.mock import patch, MagicMock

from extract_fn import fetch_rss_feed, get_article_content


class TestExtract:
    """Unit tests for the extract_fn script."""

    @patch("feedparser.parse")
    def test_fetch_rss_feed(self, mock_parse, sample_feed_data):
        """Tests the fetch_rss_feed function."""

        mock_parse.return_value = sample_feed_data
        feed = fetch_rss_feed("https://fake.url/rss")
        assert feed == sample_feed_data
        mock_parse.assert_called_once_with("https://fake.url/rss")

    @patch("grequests.get")
    def test_get_article_content(self, mock_get, sample_article_content):
        """Tests the get_article_content function."""

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = sample_article_content.encode("UTF-8")
        mock_get.return_value = mock_response

        content = get_article_content("https://www.example.com/article1")
        assert content == "This is a sample article content."
        mock_get.assert_called_once_with("https://www.example.com/article1")

    @patch("grequests.get")
    def test_get_article_content_fails(self, mock_get, sample_article_content):
        """Tests the get_article_content function."""

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.content = sample_article_content.encode("UTF-8")
        mock_get.return_value = mock_response

        content = get_article_content("https://www.example.com/article1")
        assert content == "This is a sample article content."
        mock_get.assert_called_once_with("https://www.example.com/article1")
