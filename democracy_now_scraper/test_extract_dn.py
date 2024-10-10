# pylint: skip-file

from unittest.mock import patch, MagicMock, Mock
from datetime import datetime

import pytest
from bs4 import BeautifulSoup

from extract_dn import (
    fetch_response_html,
    chunk_links,
    fetch_article_responses,
    get_article_title,
    get_headline_title,
    get_article_contents,
    get_headline_contents,
    reformat_date,
    get_headline_date,
    get_article_date,
    scrape_article,
    get_all_topic_links,
    get_all_links_from_topic,
    get_all_links_from_all_topics,
    parse_all_links,
    link_is_old,
    scrape_democracy_now
)


def test_fetch_response_html():

    mock_response = MagicMock()
    mock_response.content = '<html><body><p>Test</p></body></html>'
    result = fetch_response_html(mock_response)

    assert isinstance(result, BeautifulSoup)


@pytest.mark.parametrize("links, chunk_size, expected", [(["link1", "link2", "link3"], 2, [["link1", "link2"], ["link3"]]),
                                                         (["link1"], 1,
                                                          [["link1"]]),
                                                         (["link1", "link2", "link3"], 1, [
                                                          ["link1"], ["link2"], ["link3"]]),
                                                         ([], 2, []),
                                                         (["link1", "link2", "link3", "link4", "link5"], 3, [
                                                             ["link1", "link2", "link3"], ["link4", "link5"]]),])
def test_chunk_links(links, chunk_size, expected):
    result = chunk_links(links, chunk_size)
    assert result == expected


@patch('grequests.map')
def test_fetch_article_responses(mock_map):

    mock_response = MagicMock()

    mock_map.return_value = [mock_response]

    result = fetch_article_responses(["https://test.com"])
    assert len(result) == 1
    assert result[0] == mock_response
    mock_map.assert_called_once()


class TestArticleFunctions:
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
        <div class="container-fluid" id="story_content">
            <span class="date">October 07, 2024</span>
        </div>
        '''
        soup = BeautifulSoup(html_content, "html.parser")
        result = get_article_date(soup)
        assert result == "2024-10-07"

    def test_get_article_date_fail(self):
        html_content = '''
        <div class="container-fluid" id="story_content">
            <p>No date here</p>
        </div>
        '''
        soup = BeautifulSoup(html_content, "html.parser")
        result = get_article_date(soup)
        assert result is None

        def test_get_headline_date(self):
            html_content = '''
            <article class="headline">
                <span class="date">October 08, 2024</span>
            </article>
            '''
            soup = BeautifulSoup(html_content, "html.parser")
            result = get_headline_date(soup)
            assert result == "2024-10-08"

        def test_get_headline_date_fail(self):
            html_content = '''
            <article class="headline">
                <p>No date here</p>
            </article>
            '''
            soup = BeautifulSoup(html_content, "html.parser")
            result = get_headline_date(soup)
            assert result is None


@pytest.mark.parametrize("input_date, expected_output", [("October 07, 2024",
                                                          "2024-10-07"),
                                                         ("Oct 07, 2024",
                                                          "2024-10-07"),
                                                         ("February 29, 2024",
                                                          "2024-02-29"),
                                                         ("Mar 15, 2023",
                                                          "2023-03-15"),
                                                         ("Invalid Date", None),
                                                         ("April 31, 2024", None),])
def test_reformat_date(input_date, expected_output):
    assert reformat_date(input_date) == expected_output


class TestScrapeArticle:

    @patch('extract_dn.get_headline_date')
    @patch('extract_dn.get_headline_contents')
    @patch('extract_dn.get_headline_title')
    @patch('extract_dn.fetch_response_html')
    def test_scrape_article_pass_headline(self, mock_fetch_response_html, mock_get_headline_title, mock_get_headline_contents, mock_get_headline_date):

        mock_fetch_response_html.return_value = Mock()
        mock_get_headline_title.return_value = "Test Headline Title"
        mock_get_headline_contents.return_value = "Headline first paragraph.\nHeadline second paragraph."
        mock_get_headline_date.return_value = "2024-10-07"

        mock_response = Mock()
        mock_response.url = 'https://www.democacrynow.org/headlines/test-article'

        result = scrape_article(mock_response)
        expected = {
            "title": "Test Headline Title",
            "content": "Headline first paragraph.\nHeadline second paragraph.",
            "link": "https://www.democacrynow.org/headlines/test-article",
            "published": "2024-10-07"
        }
        assert result == expected

    @patch('extract_dn.get_article_date')
    @patch('extract_dn.get_article_contents')
    @patch('extract_dn.get_article_title')
    @patch('extract_dn.fetch_response_html')
    def test_scrape_article_pass_regular_article(self, mock_fetch_response_html, mock_get_article_title, mock_get_article_contents, mock_get_article_date):

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
            "link": "https://www.democacrynow.org/articles/test-article",
            "published": "2024-10-08"
        }
        assert result == expected

    @patch('extract_dn.get_article_date')
    @patch('extract_dn.get_article_contents')
    @patch('extract_dn.get_article_title')
    @patch('extract_dn.fetch_response_html')
    def test_scrape_article_fail(self, mock_fetch_response_html, mock_get_article_title, mock_get_article_contents, mock_get_article_date):

        mock_fetch_response_html.return_value = Mock()
        mock_get_article_title.return_value = None
        mock_get_article_contents.return_value = None
        mock_get_article_date.return_value = "2024-10-07"

        mock_response = Mock()
        mock_response.url = 'https://www.democacrynow.org/articles/test-article'

        result = scrape_article(mock_response)
        expected = "Failed to fetch content from https://www.democacrynow.org/articles/test-article"
        assert result == expected


class TestGetAllTopicLinks():

    @patch('extract_dn.fetch_response_html')
    @patch('extract_dn.fetch_article_responses')
    def test_get_all_topic_links(self, mock_fetch_article_responses, mock_fetch_response_html):

        html_content = """
            <html>
                <body>
                    <div class="container-fluid"></div>
                    <div class="container-fluid"></div>
                    <div class="container-fluid"></div>
                    <div class="container-fluid"></div>
                    <div class="container-fluid">
                        <li><a href="/topic/1">Topic 1</a></li>
                        <li><a href="/topic/2">Topic 2</a></li>
                    </div>
                </body>
            </html>
        """
        mock_fetch_article_responses.return_value = [True]
        mock_fetch_response_html.return_value = BeautifulSoup(html_content,
                                                              'html.parser')

        result = get_all_topic_links()
        expected = ["https://www.democracynow.org/topic/1",
                    "https://www.democracynow.org/topic/2"]
        assert result == expected

    @patch('extract_dn.fetch_article_responses')
    def test_get_all_topic_links_fail(self, mock_fetch_article_responses):

        mock_fetch_article_responses.return_value = [None]

        result = get_all_topic_links()
        expected = []
        assert result == expected


@patch('extract_dn.fetch_response_html')
def test_get_all_links_from_topic(mock_fetch_response_html):
    html_content = """
        <html>
            <body>
                <a data-ga-action="Topic: Story Headline" href="/article1">Article 1</a>
                <a data-ga-action="Topic: Story Headline" href="/article2">Article 2</a>
                <a data-ga-action="Other Action" href="/article3">Article 3</a>
            </body>
        </html>
    """
    mock_response = Mock()
    mock_response.content = html_content.encode('utf-8')

    mock_fetch_response_html.return_value = BeautifulSoup(
        html_content, 'html.parser')

    result = get_all_links_from_topic(mock_response)
    expected = [
        "https://www.democracynow.org/article1",
        "https://www.democracynow.org/article2"
    ]
    assert result == expected


class TestGetAllLinksFromAllTopics:

    @patch('extract_dn.get_all_links_from_topic')
    @patch('extract_dn.fetch_article_responses')
    @patch('extract_dn.get_all_topic_links')
    def test_get_all_links_from_all_topics(self, mock_get_all_topic_links, mock_fetch_article_responses, mock_get_all_links_from_topic):
        topic_links = ["https://www.democracynow.org/topic/1",
                       "https://www.democracynow.org/topic/2"]
        mock_response_1 = Mock()
        mock_response_2 = Mock()

        mock_get_all_topic_links.return_value = topic_links
        mock_fetch_article_responses.return_value = [mock_response_1,
                                                     mock_response_2]
        mock_get_all_links_from_topic.side_effect = [["https://www.democracynow.org/article1",
                                                      "https://www.democracynow.org/article2"],
                                                     ["https://www.democracynow.org/article3"]]

        result = get_all_links_from_all_topics()
        expected = ["https://www.democracynow.org/article1",
                    "https://www.democracynow.org/article2",
                    "https://www.democracynow.org/article3"]
        assert result == expected

    @patch('extract_dn.get_all_topic_links')
    def test_get_all_links_from_all_topics_fail(self, mock_get_all_topic_links):
        mock_get_all_topic_links.return_value = []

        result = get_all_links_from_all_topics()
        expected = []
        assert result == expected


class TestParseAllLinks:

    @patch('extract_dn.scrape_article')
    @patch('extract_dn.fetch_article_responses')
    def test_parse_all_links(self, mock_fetch_article_responses, mock_scrape_article):
        all_links = ["https://www.democracynow.org/article1",
                     "https://www.democracynow.org/article2"]

        mock_fetch_article_responses.return_value = [Mock(), Mock()]
        mock_scrape_article.side_effect = [{"title": "Article 1", "content": "Content of article 1",
                                            "link": "https://www.democracynow.org/article1", "published": "2024-10-01"},
                                           {"title": "Article 2", "content": "Content of article 2",
                                            "link": "https://www.democracynow.org/article2", "published": "2024-10-02"}]

        result = parse_all_links(all_links)
        expected = [{"title": "Article 1", "content": "Content of article 1",
                     "link": "https://www.democracynow.org/article1", "published": "2024-10-01"},
                    {"title": "Article 2", "content": "Content of article 2",
                     "link": "https://www.democracynow.org/article2", "published": "2024-10-02"}]
        assert result == expected

    @patch('extract_dn.scrape_article')
    @patch('extract_dn.fetch_article_responses')
    def test_parse_all_links_fail(self, mock_fetch_article_responses, mock_scrape_article):
        all_links = ["https://www.democracynow.org/article1",
                     "https://www.democracynow.org/article2"]

        mock_fetch_article_responses.return_value = [None, None]

        result = parse_all_links(all_links)
        expected = []
        assert result == expected


class TestLinkIsOld:
    @pytest.mark.parametrize("link, time_diff, date, expected", [("https://www.democracynow.org/2023/10/1/story", 7,
                                                                  datetime(2023, 10, 1), False),
                                                                 ("https://www.democracynow.org/2022/9/25/story", 7,
                                                                  datetime(2023, 9, 25), True)])
    @patch('extract_dn.datetime')
    def test_link_is_old(self, mock_datetime, link, time_diff, date, expected):

        mock_datetime.now.return_value = datetime(2023, 10, 6)
        mock_datetime.strptime.return_value = date

        result = link_is_old(link, time_diff)
        assert result == expected

    def test_link_is_old_throws_value_error(self):

        result = link_is_old("https://www.democracynow.org/n/o_/dat/e/story",
                             7)
        assert result == True


@patch('extract_dn.parse_all_links')
@patch('extract_dn.link_is_old')
@patch('extract_dn.get_all_links_from_all_topics')
def test_scrape_democracy_now(mock_get_all_links, mock_link_is_old, mock_parse_all_links):
    # Setup mock return values
    mock_get_all_links.return_value = ["https://www.democracynow.org/2024/10/1/story",
                                       "https://www.democracynow.org/2023/9/25/story",
                                       "https://www.democracynow.org/invalid/date"]

    mock_link_is_old.side_effect = [False, True, True]
    mock_parse_all_links.return_value = [{"title": "Story 1", "content": "Content 1"},
                                         {"title": "Story 2", "content": "Content 2"},]

    result = scrape_democracy_now(7)

    mock_get_all_links.assert_called_once()
    mock_link_is_old.assert_any_call(
        "https://www.democracynow.org/2024/10/1/story", 7)
    mock_link_is_old.assert_any_call(
        "https://www.democracynow.org/invalid/date", 7)
    mock_parse_all_links.assert_called_once()

    assert len(result) == 2
    assert result == [{"title": "Story 1", "content": "Content 1"},
                      {"title": "Story 2", "content": "Content 2"},]
