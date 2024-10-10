# pylint: skip-file

from unittest.mock import patch, MagicMock, Mock
from datetime import datetime

import pytest
from bs4 import BeautifulSoup

from extract_dn import (
    fetch_response_html,
    fetch_article_responses,
    get_article_title,
    get_headline_title,
    get_article_contents,
    get_headline_contents,
    reformat_date,
    get_article_date,
    scrape_article,
    get_all_topic_links,
    get_all_links_from_topic,
    link_is_old
)


def test_fetch_response_html():

    mock_response = MagicMock()
    mock_response.content = '<html><body><p>Test</p></body></html>'
    result = fetch_response_html(mock_response)

    assert isinstance(result, BeautifulSoup)


@patch('grequests.map')
def test_fetch_article_responses(mock_map):
    mock_response = MagicMock()
    mock_map.return_value = [mock_response]

    result = fetch_article_responses(["https://test.com"])
    assert len(result) == 1
    assert result[0] == mock_response
    mock_map.assert_called_once()


class TestGetArticleTitle:

    def test_get_article_title(self):

        html_content = '''
        <div class="container-fluid" id="story_content">
            <h1>Test Article Title</h1>
        </div>
        '''
        soup = BeautifulSoup(html_content, "html.parser")
        result = get_article_title(soup)

        assert result == "Test Article Title"

    def test_get_article_title_fail(self):

        html_content = '''
        <div class="container-fluid" id="story_content">
            <p>No title here</p>
        </div>
        '''
        soup = BeautifulSoup(html_content, "html.parser")
        result = get_article_title(soup)

        assert result is None


class TestArticleFunctions:

    def test_get_headline_title(self):
        html_content = '''
        <article class="headline">
            <h1>Test Headline Title</h1>
        </article>
        '''
        soup = BeautifulSoup(html_content, "html.parser")
        result = get_headline_title(soup)
        assert result == "Test Headline Title"

    def test_get_headline_title_fail(self):
        html_content = '''
        <article class="headline">
            <p>No title here</p>
        </article>
        '''
        soup = BeautifulSoup(html_content, "html.parser")
        result = get_headline_title(soup)
        assert result is None

    def test_get_article_contents(self):
        html_content = '''
        <div class="story_summary">
            <p>First paragraph.</p>
            <p>Second paragraph.</p>
        </div>
        <div class="mobile_anchor_target" id="transcript">
            <p>Transcript paragraph.</p>
        </div>
        '''
        soup = BeautifulSoup(html_content, "html.parser")
        result = get_article_contents(soup)
        assert result == "First paragraph.\nSecond paragraph.\nTranscript paragraph."

    def test_get_article_contents_fail(self):
        html_content = '''
        <div class="story_summary">
            <p>No content here.</p>
        </div>
        '''
        soup = BeautifulSoup(html_content, "html.parser")
        result = get_article_contents(soup)
        assert result is None

    def test_get_headline_contents(self):
        html_content = '''
        <div class="headline_summary">
            <p>Headline first paragraph.</p>
            <p>Headline second paragraph.</p>
        </div>
        '''
        soup = BeautifulSoup(html_content, "html.parser")
        result = get_headline_contents(soup)
        assert result == "Headline first paragraph.\nHeadline second paragraph."

    def test_get_headline_contents_fail(self):
        html_content = '''
        <div class="other_summary">
            <p>No headline content here.</p>
        </div>
        '''
        soup = BeautifulSoup(html_content, "html.parser")
        result = get_headline_contents(soup)
        assert result is None

    def test_get_article_date(self):
        html_content = '''
        <span class="date">October 07, 2024</span>
        '''
        soup = BeautifulSoup(html_content, "html.parser")
        result = get_article_date(soup)
        assert result == "2024-10-07"

    def test_get_article_date_fail(self):
        html_content = '''
        <div class="date-container">
            <p>No date here</p>
        </div>
        '''
        soup = BeautifulSoup(html_content, "html.parser")
        result = get_article_date(soup)
        assert result is None


class TestScrapeArticle():

    @patch('extract_dn.fetch_response_html')
    @patch('extract_dn.get_headline_title')
    @patch('extract_dn.get_headline_contents')
    @patch('extract_dn.get_article_date')
    def test_scrape_article_pass_headline(self, mock_get_article_date, mock_get_headline_contents, mock_get_headline_title, mock_fetch_response_html):
        mock_fetch_response_html.return_value = Mock()
        mock_get_headline_title.return_value = "Test Headline Title"
        mock_get_headline_contents.return_value = "Headline first paragraph.\nHeadline second paragraph."
        mock_get_article_date.return_value = "2024-10-07"

        mock_response = Mock()
        mock_response.url = 'https://www.democacrynow.org/headlines/test-article'

        result = scrape_article(mock_response)
        expected = {
            "title": "Test Headline Title",
            "content": "Headline first paragraph.\nHeadline second paragraph.",
            "link:": "https://www.democacrynow.org/headlines/test-article",
            "published": "2024-10-07"
        }
        assert result == expected

    @patch('extract_dn.fetch_response_html')
    @patch('extract_dn.get_article_title')
    @patch('extract_dn.get_article_contents')
    @patch('extract_dn.get_article_date')
    def test_scrape_article_pass_regular_article(self, mock_get_article_date, mock_get_article_contents, mock_get_article_title, mock_fetch_response_html):
        mock_fetch_response_html.return_value = Mock()
        mock_get_article_title.return_value = "Test Article Title"
        mock_get_article_contents.return_value = "First paragraph.\nSecond paragraph."
        mock_get_article_date.return_value = "2024-10-08"

        mock_response = Mock()
        mock_response.url = 'https://www.democacrynow.org/articles/test-article'

        result = scrape_article(mock_response)
        expected = {
            "title": "Test Article Title",
            "content": "First paragraph.\nSecond paragraph.",
            "link:": "https://www.democacrynow.org/articles/test-article",
            "published": "2024-10-08"
        }
        assert result == expected

    @patch('extract_dn.fetch_response_html')
    @patch('extract_dn.get_article_title')
    @patch('extract_dn.get_article_contents')
    @patch('extract_dn.get_article_date')
    def test_scrape_article_fail(self, mock_get_article_date, mock_get_article_contents, mock_get_article_title, mock_fetch_response_html):
        mock_fetch_response_html.return_value = Mock()
        mock_get_article_title.return_value = None
        mock_get_article_contents.return_value = None
        mock_get_article_date.return_value = "2024-10-07"

        mock_response = Mock()
        mock_response.url = 'https://www.democacrynow.org/articles/test-article'

        result = scrape_article(mock_response)
        expected = "Failed to fetch content from https://www.democacrynow.org/articles/test-article"
        assert result == expected
