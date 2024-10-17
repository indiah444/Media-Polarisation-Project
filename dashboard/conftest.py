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
    """Returns an example dataframe"""
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
