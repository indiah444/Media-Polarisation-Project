# pylint: skip-file

import pytest
import pandas as pd
import altair as alt


@pytest.fixture
def sample_data():

    data = {
        'topic_name': ['Topic A', 'Topic B', 'Topic C'],
        'avg_polarity_score': [0.1, 0.5, -0.3],
        'source_name': ['Fox News', 'Democracy Now!', 'Fox News']
    }

    return pd.DataFrame(data)


@pytest.fixture
def sample_chart():

    df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    chart = alt.Chart(df).mark_line().encode(x='x', y='y')
    return chart
