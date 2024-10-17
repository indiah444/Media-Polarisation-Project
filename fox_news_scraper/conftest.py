# pylint: skip-file

import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def sample_feed_data():
    """Fixture for sample RSS feed data."""
    return {
        "entries": [
            {
                "title": "Sample Article 1",
                "link": "https://www.example.com/article1",
                "published": "2024-01-01T00:00:00Z"
            },
            {
                "title": "Sample Article 2",
                "link": "https://www.example.com/article2",
                "published": "2024-01-02T00:00:00Z"
            }
        ]
    }


@pytest.fixture
def sample_article_content():
    """Fixture for sample article content."""
    return "<div class='article-body'>This is a sample article content.</div>"


@pytest.fixture
def mock_feed():
    """Fixture to create a mock feed with sample entries."""
    feed = MagicMock()
    feed.entries = [
        MagicMock(title="Article 1",
                  link="http://example.com/article1", published="2024-10-10"),
        MagicMock(title="Article 2",
                  link="http://example.com/article2", published="2024-10-11")
    ]
    return feed


@pytest.fixture
def mock_responses():
    """Fixture to create mock responses for successful and unsuccessful cases."""
    mock_response_1 = MagicMock(status_code=200)
    mock_response_2 = MagicMock(status_code=404)
    return [mock_response_1, mock_response_2]


@pytest.fixture
def mock_parse_article_content():
    """Fixture to mock the parse_article_content function."""
    with patch('extract_fn.parse_article_content') as mock:
        yield mock


@pytest.fixture
def mock_grequests():
    """Fixture to mock grequests.get and grequests.map."""
    with patch('extract_fn.grequests.get') as mock_get:
        with patch('extract_fn.grequests.map') as mock_map:
            yield mock_get, mock_map


@pytest.fixture
def mock_parse_feed_entries():
    with patch('extract_fn.parse_feed_entries') as mock:
        yield mock
