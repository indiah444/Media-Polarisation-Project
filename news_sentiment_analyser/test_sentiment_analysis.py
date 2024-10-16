# pylint: skip-file

"""Tests sentiment analysis script"""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

from sentiment_analysis import get_sentiments, get_avg_sentiment


@pytest.fixture
def sample_df():
    """Mocks a valid dataframe"""
    return pd.DataFrame({
        'text': ["123", "456", "789"],
        'topic': ['a', 'b', 'c'],
        'source': ['source1', 'source1', 'source2']
    })


@pytest.fixture
def mock_sia():
    """Mocks the string intensity analyser."""

    with patch('sentiment_analysis.SentimentIntensityAnalyzer') as mock:
        mock_instance = MagicMock()
        mock_instance.polarity_scores.side_effect = [
            {'pos': 0.6369, 'neg': 0.0, 'neu': 0.3631, 'compound': 0.6369},
            {'pos': 0.0, 'neg': 0.4939, 'neu': 0.5061, 'compound': -0.4404},
            {'pos': 0.0, 'neg': 0.0, 'neu': 1.0, 'compound': 0.0},
            {'pos': 0.6369, 'neg': 0.0, 'neu': 0.3631, 'compound': 0.6369}
        ]
        yield mock_instance


def test_get_sentiments_correct_cols(mock_sia, sample_df):
    """Asserts that get_sentiments returns a dataframe with the correct columns"""

    sentiments = get_sentiments(mock_sia, sample_df, 'text')

    assert 'pos' in sentiments.columns
    assert 'neg' in sentiments.columns
    assert 'neut' in sentiments.columns
    assert 'compound' in sentiments.columns


def test_get_sentiments_correct_vals(mock_sia, sample_df):
    """Asserts that get_sentiments returns a dataframe with the correct values"""

    sentiments = get_sentiments(mock_sia, sample_df, 'text')

    assert pytest.approx(sentiments['pos'][0], rel=1e-4) == 0.6369
    assert pytest.approx(sentiments['neg'][1], rel=1e-4) == 0.4939


def test_get_sentiments_type_error():
    """Tests that a TypeError is raised if the 'text' column
    contains non-string objects"""

    df_non_string = pd.DataFrame({
        'text': [123, 456, 789],
        'topic': ['a', 'b', 'c'],
        'source': ['source1', 'source1', 'source2']
    })

    with pytest.raises(TypeError):
        get_sentiments(MagicMock(), df_non_string, 'text')


def test_get_sentiments_type_error_mixed_types():
    """Tests that a TypeError is raised if the 'text' column
    contains non-string objects"""

    df_non_string = pd.DataFrame({
        'text': [123, "456", 789],
        'topic': ['a', 'b', 'c'],
        'source': ['source1', 'source1', 'source2']
    })

    with pytest.raises(TypeError):
        get_sentiments(MagicMock(), df_non_string, 'text')


def test_get_avg_sentiment_correct_shape(mock_sia, sample_df):
    """Asserts that get_avg_sentiment returns a dataframe
    of the correct shape."""

    sentiments = get_sentiments(mock_sia, sample_df, 'text')

    avg_sentiments = get_avg_sentiment(sentiments, 'topic', 'source')

    assert avg_sentiments.shape[0] == 3


def test_get_avg_sentiment_correct_values(mock_sia, sample_df):
    """Asserts that get_avg_sentiment returns a dataframe
    with the correct values."""

    sentiments = get_sentiments(mock_sia, sample_df, 'text')

    avg_sentiments = get_avg_sentiment(sentiments, 'topic', 'source')

    assert pytest.approx(avg_sentiments['pos'][0], rel=1e-4) == 0.6369
    assert pytest.approx(avg_sentiments['neg'][1], rel=1e-4) == 0.4939
