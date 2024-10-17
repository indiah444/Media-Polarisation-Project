import pytest


@pytest.fixture
def fake_data():
    return {
        'source_name': ['Fox News', 'Democracy Now!', 'Fox News'],
        'avg_polarity_score': [0.2, 0.5, -0.1],
        'article_count': [100, 150, 80]
    }
