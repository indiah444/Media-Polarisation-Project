"""Script to create the graphs to be sent as an email."""
from io import BytesIO
import base64

import altair as alt
import pandas as pd


def create_sentiment_distribution_chart(df):
    """Creates a distribution graph of average score by topic and source
    Returns as a base64 image."""
    df['article_count'] = df.groupby(['topic_name', 'source_name'])[
        'avg_polarity_score'].transform('count')
    points = alt.Chart(df).mark_circle().encode(
        x='avg_polarity_score:Q',
        y='topic_name:O',
        color='source_name:N',
        size=alt.Size('article_count:Q', legend=None, scale=alt.Scale(
            range=[30, 300])),  # Set size based on article count
        tooltip=['topic_name', 'source_name',
                 'avg_polarity_score', 'article_count']
    ).properties(
        width=400,
        height=300
    )
    vertical_line = alt.Chart(pd.DataFrame({'x': [0]})).mark_rule(color='black').encode(
        x='x:Q'
    )
    chart = alt.layer(points, vertical_line)

    return chart_to_base64(chart)


def create_bar_graph(df):
    """Creates a bar chart of scores.
    Returns as a base64 image."""
    base_chart = alt.Chart(df).properties(
        width=150,
        height=200
    )
    bars = base_chart.mark_bar().encode(
        x='avg_polarity_score:Q',
        y='topic_name:O',
        color='avg_polarity_score:Q',
        tooltip=['topic_name', 'source_name', 'avg_polarity_score']
    )
    vertical_line = alt.Chart(pd.DataFrame({'x': [0]})).mark_rule(color='black').encode(
        x='x:Q'
    )
    layered_chart = alt.layer(bars, vertical_line)
    faceted_chart = layered_chart.facet(
        column='source_name:N',
        data=df
    ).configure_axis(
        grid=False
    ).configure_view(
        strokeWidth=0
    )

    return chart_to_base64(faceted_chart)


def chart_to_base64(chart):
    """Converts chart to base64 image so can be emailed."""
    chart_image = BytesIO()
    chart.save(chart_image, format='png')
    chart_image.seek(0)
    base64_img = base64.b64encode(chart_image.read()).decode('utf-8')
    return base64_img
