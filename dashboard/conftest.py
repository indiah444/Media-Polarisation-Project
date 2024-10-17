# pylint: skip-file

import pytest
import pandas as pd


@pytest.fixture
def fake_aggregated_data():
    return {
        'source_name': ['Fox News', 'Democracy Now!', 'Fox News'],
        'avg_polarity_score': [0.2, 0.5, -0.1],
        'article_count': [100, 150, 80]
    }


@pytest.fixture
def fake_data():
    return {
        'source_name': ['Fox News', 'Democracy Now!', 'Fox News', 'Democracy Now!', 'Fox News'],
        'title_polarity_score': [-0.5, 0.7, 0.2, -0.3, 0.1],
        'content_polarity_score': [0.4, -0.6, 0.3, 0.8, -0.2],
        'topic_name': ['Trump', 'Kamala', 'Climate Change', 'Economy', 'Palestine'],
        'date_published': pd.date_range(start='2023-01-01', periods=5, freq='D')
    }
