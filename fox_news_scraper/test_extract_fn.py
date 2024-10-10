"""Test file for functions in extract_fn.py"""
import pytest
from unittest.mock import patch, MagicMock
from unittest import TestCase
from bs4 import BeautifulSoup
from extract_fn import fetch_rss_feed, get_article_content, remove_hyperlink_ads, parse_article_content


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


class TestParseArticleContent(TestCase):

    @patch('extract_fn.remove_hyperlink_ads')
    def test_valid_article_content(self, mock_remove_hyperlink_ads):
        """Tests the case of valid responses"""

        mock_response = MagicMock()
        mock_response.content = """
        <div class="article-body">
        <p>This is the article content.</p>
        </div>"""

        mock_soup = BeautifulSoup(mock_response.content, "html.parser")
        mock_remove_hyperlink_ads.return_value = mock_soup

        result = parse_article_content(mock_response)
        self.assertEqual(result, "This is the article content.")

    @patch('extract_fn.remove_hyperlink_ads')
    def test_calls_remove_hyperlink(self, mock_remove_hyperlink_ads):
        """Tests the case of valid responses"""

        mock_response = MagicMock()
        mock_response.content = """
        <div class="article-body">
        <p>This is the article content.</p>
        </div>"""

        mock_soup = BeautifulSoup(mock_response.content, "html.parser")
        parse_article_content(mock_response)
        mock_remove_hyperlink_ads.assert_called_once_with(mock_soup)

    @patch('extract_fn.find_article_body')
    @patch('extract_fn.remove_hyperlink_ads')
    def test_article_body_not_found(self, mock_remove_hyperlink_ads, mock_find_article_body):
        """Test the case of an article body not found"""
        mock_response = MagicMock()
        mock_response.content = "<html><body><div>No article here</div></body></html>"

        mock_soup = BeautifulSoup(mock_response.content, "html.parser")
        mock_remove_hyperlink_ads.return_value = mock_soup

        mock_find_article_body.return_value = None

        result = parse_article_content(mock_response)
        self.assertEqual(result, "Full content not found or unable to parse.")


class TestExtract:
    """Unit tests for the extract_fn script."""

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
