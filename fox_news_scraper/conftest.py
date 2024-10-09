import pytest


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
