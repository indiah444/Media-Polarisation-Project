# pylint: skip-file

from datetime import datetime

import pytest
import pandas as pd


@pytest.fixture
def fake_date_published():
    return {
        "date_published": [
            pd.Timestamp("2024-10-18"),  # A random date
            pd.Timestamp("2020-02-29"),  # Leap year date
            pd.Timestamp("2024-01-01"),  # Start of the year
            pd.Timestamp("2024-12-31")   # End of the year
        ]
    }


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


@pytest.fixture
def fake_heatmap_data():
    return {
        'source_name': ['Fox News', 'Democracy Now!', 'Fox News', 'Democracy Now!', 'Fox News'],
        'title_polarity_score': [-0.5, 0.7, 0.2, -0.3, 0.1],
        'content_polarity_score': [0.4, -0.6, 0.3, 0.8, -0.2],
        'topic_name': ['Trump', 'Kamala', 'Climate Change', 'Economy', 'Palestine'],
        'date_name': ['2024-10-17', '2024-10-24', '2024-11-01', '2024-11-08', '2024-11-15'],
        'week_num': [42, 43, 44, 45, 46],
        'week_text': ['Week 42', 'Week 43', 'Week 44', 'Week 45', 'Week 46'],
        'weekday': ['Thursday', 'Thursday', 'Friday', 'Friday', 'Friday'],
    }


@pytest.fixture
def example_df():
    return pd.DataFrame(
        [
            {'topic_name': 'Donald Trump',
             'source_name': 'Fox News',
             'content_polarity_score': 0.0,
             'title_polarity_score': -0.3712,
             'date_published': datetime.date(2024, 10, 10)},
            {'topic_name': 'Donald Trump',
             'source_name': 'Fox News',
             'content_polarity_score': -0.9781,
             'title_polarity_score': -0.3612,
             'date_published': datetime.date(2024, 10, 9)}

        ])


@pytest.fixture
def sample_df():
    data = {'Fox News': [0.7, -0.6, 'N/A'],
            'Democracy Now!': [-0.8, 0.3, 'N/A']}
    index = ['Topic 1', 'Topic 2', 'Topic 3']
    return pd.DataFrame(data, index=index)
