"""Test file for functions in extract_fn.py"""
import pytest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from extract_fn import fetch_rss_feed, get_article_content, remove_hyperlink_ads


@pytest.mark.parametrize("fake_url", [
    ("https://fake.url/rss"),
    (""),
    ("malformed_url")
])
@patch("feedparser.parse")
def test_fetch_rss_feed(mock_parse, sample_feed_data, fake_url):
    """Tests the fetch_rss_feed function."""

    mock_parse.return_value = sample_feed_data
    feed = fetch_rss_feed(fake_url)

    assert feed == sample_feed_data

    mock_parse.assert_called_once_with(fake_url)


@patch('feedparser.parse')
def test_valid_feed_url(mock_parse, sample_feed_data):
    """Tests the fetch_rss_feed returns the correct output"""
    mock_parse.return_value = sample_feed_data
    result = fetch_rss_feed("https://example.com/rss")
    assert result == sample_feed_data


def test_feed_url_is_not_string():
    """Test for invalid non-string input"""
    with pytest.raises(TypeError):
        fetch_rss_feed(123)


def test_feed_url_is_a_boolean():
    """Test for invalid non-string input"""
    with pytest.raises(TypeError):
        fetch_rss_feed(True)


@pytest.mark.parametrize("html, expected", [
    ("<a><strong>...</strong></a>", ""),
    ("<a><strong>This is an ad</strong></a>", ""),
    ("<a>This is not an ad</a>", "This is not an ad"),
    ("<strong>This is not an ad</strong>", "This is not an ad")
])
def test_remove_hyperlink_ads(html, expected):
    """Test with a simple case of <a><strong>...</strong></a>"""
    parsed = BeautifulSoup(html, 'html.parser')
    assert remove_hyperlink_ads(parsed).get_text() == expected


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
