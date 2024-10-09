"""Tests sentiment analysis script"""

import pytest
from sentiment_analysis import get_sentiments


def test_get_sentiments_type_error():
    # Create a DataFrame with non-string text
    df_non_string = pd.DataFrame({
        'text': [123, 456, 789],
        'topic': ['a', 'b', 'c'],
        'source': ['source1', 'source1', 'source2']
    })

    with pytest.raises(TypeError):
        get_sentiments(MagicMock(), df_non_string, 'text', 'topic', 'source')
