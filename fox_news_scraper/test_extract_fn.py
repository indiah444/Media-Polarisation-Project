# pylint: skip-file

"""Test file for functions in extract_fn.py"""

from unittest.mock import patch, MagicMock
from unittest import TestCase

import pytest
from bs4 import BeautifulSoup
from extract_fn import fetch_rss_feed, get_article_content, remove_hyperlink_ads, parse_article_content, parse_feed_entries, fetch_from_multiple_feeds


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


class TestGetArticleContent:

    @patch('extract_fn.parse_article_content')
    @patch('extract_fn.grequests.get')
    def test_successful_fetch(self, mock_get, mock_parse_article_content):
        """Test when the article content is fetched successfully."""

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_parse_article_content.return_value = "This is the article content"
        mock_get.return_value = mock_response

        result = get_article_content("http://example.com/article")
        assert result == "This is the article content"

    @patch('extract_fn.grequests.get')
    def test_non_200_status_code(self, mock_get):
        """Test when the request returns a non-200 status code."""

        mock_response = MagicMock()
        mock_response.status_code = 404  # Simulate a 404 error
        mock_get.return_value = mock_response

        result = get_article_content("http://example.com/article")
        assert result == "Couldn't connect to article, status_code: 404"

    @patch('extract_fn.grequests.get')
    def test_exception_handling(self, mock_get):
        """Test when an exception occurs during the request."""

        mock_get.side_effect = Exception(
            "Connection error")  # Simulate an exception

        result = get_article_content("http://example.com/article")
        assert result == "Failed to fetch full content from http://example.com/article: Connection error"

    @patch('extract_fn.parse_article_content')
    @patch('extract_fn.grequests.get')
    def test_parse_article_content_failure(self, mock_get, mock_parse_article_content):
        """Test when the article is fetched but parsing fails."""

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_parse_article_content.side_effect = Exception(
            "Parsing error")  # Simulate a parsing error
        mock_get.return_value = mock_response

        result = get_article_content("http://example.com/article")
        assert result == "Failed to fetch full content from http://example.com/article: Parsing error"


class TestParseFeedEntries:

    def test_successful_entries(self, mock_feed, mock_grequests, mock_parse_article_content):
        """Test when all entries are fetched and parsed successfully."""

        mock_get, mock_map = mock_grequests

        mock_map.return_value = [
            MagicMock(status_code=200),
            MagicMock(status_code=200)
        ]

        mock_parse_article_content.side_effect = [
            "Content for article 1", "Content for article 2"]

        result = parse_feed_entries(mock_feed)

        expected = [
            {
                "title": "Article 1",
                "content": "Content for article 1",
                "link": "http://example.com/article1",
                "published": "2024-10-10",
                "source_name": "Fox News"
            },
            {
                "title": "Article 2",
                "content": "Content for article 2",
                "link": "http://example.com/article2",
                "published": "2024-10-11",
                "source_name": "Fox News"
            }
        ]

        assert result == expected

    def test_non_200_status_code(self, mock_feed, mock_grequests, mock_parse_article_content):
        """Test when one of the entries returns a non-200 status code."""

        mock_get, mock_map = mock_grequests

        mock_map.return_value = [
            MagicMock(status_code=200),
            MagicMock(status_code=404)
        ]

        mock_parse_article_content.return_value = "Content for article 1"

        result = parse_feed_entries(mock_feed)

        expected = [
            {
                "title": "Article 1",
                "content": "Content for article 1",
                "link": "http://example.com/article1",
                "published": "2024-10-10",
                "source_name": "Fox News"
            },
            {
                "title": "Article 2",
                "content": "Couldn't connect to article, status_code: 404",
                "link": "http://example.com/article2",
                "published": "2024-10-11",
                "source_name": "Fox News"
            }
        ]

        assert result == expected

    def test_no_response(self, mock_feed, mock_grequests, mock_parse_article_content):
        """Test when no response is returned for an entry."""

        mock_get, mock_map = mock_grequests

        mock_map.return_value = [
            MagicMock(status_code=200),
            None
        ]

        mock_parse_article_content.return_value = "Content for article 1"

        result = parse_feed_entries(mock_feed)

        expected = [
            {
                "title": "Article 1",
                "content": "Content for article 1",
                "link": "http://example.com/article1",
                "published": "2024-10-10",
                "source_name": "Fox News"
            },
            {
                "title": "Article 2",
                "content": "Couldn't connect to article, status_code: No response.",
                "link": "http://example.com/article2",
                "published": "2024-10-11",
                "source_name": "Fox News"
            }
        ]

        assert result == expected


class TestFetchFromMultipleFeeds:

    def test_fetch_from_multiple_feeds_success(self, mock_grequests, mock_parse_feed_entries):
        """Test fetching from multiple feeds successfully."""

        _, mock_map = mock_grequests

        feed_urls = ["http://example.com/feed1", "http://example.com/feed2"]

        mock_response_1 = MagicMock(status_code=200, content=b"<xml>...</xml>")
        mock_response_2 = MagicMock(status_code=200, content=b"<xml>...</xml>")

        mock_map.return_value = [mock_response_1, mock_response_2]

        mock_parse_feed_entries.side_effect = [
            [{"title": "Entry 1", "content": "Content 1", "link": "http://example.com/entry1",
                "published": "2024-10-10", "source_name": "Source 1"}],
            [{"title": "Entry 2", "content": "Content 2", "link": "http://example.com/entry2",
                "published": "2024-10-11", "source_name": "Source 2"}]
        ]

        result = fetch_from_multiple_feeds(feed_urls)

        # Expected output
        expected = [
            {"title": "Entry 1", "content": "Content 1", "link": "http://example.com/entry1",
                "published": "2024-10-10", "source_name": "Source 1"},
            {"title": "Entry 2", "content": "Content 2", "link": "http://example.com/entry2",
                "published": "2024-10-11", "source_name": "Source 2"}
        ]

        assert result == expected

    def test_fetch_from_multiple_feeds_failure(self, mock_grequests, mock_parse_feed_entries):
        """Test handling failures when fetching from feeds."""

        _, mock_map = mock_grequests

        feed_urls = ["http://example.com/feed1", "http://example.com/feed2"]

        mock_response_1 = MagicMock(status_code=200, content=b"<xml>...</xml>")
        mock_response_2 = MagicMock(status_code=404, content=b"<xml>...</xml>")

        mock_map.return_value = [mock_response_1, mock_response_2]

        mock_parse_feed_entries.return_value = [{"title": "Entry 1", "content": "Content 1",
                                                 "link": "http://example.com/entry1", "published": "2024-10-10", "source_name": "Source 1"}]

        result = fetch_from_multiple_feeds(feed_urls)

        expected = [
            {"title": "Entry 1", "content": "Content 1", "link": "http://example.com/entry1",
                "published": "2024-10-10", "source_name": "Source 1"}
        ]

        assert result == expected

    def test_fetch_from_multiple_feeds_no_responses(self, mock_grequests):
        """Test when no responses are returned."""

        _, mock_map = mock_grequests

        feed_urls = ["http://example.com/feed1", "http://example.com/feed2"]

        mock_map.return_value = [None, None]

        result = fetch_from_multiple_feeds(feed_urls)
        expected = []
        assert result == expected
