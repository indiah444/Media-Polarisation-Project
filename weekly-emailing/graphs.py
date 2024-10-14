"""Script to create the graphs to be sent as an email."""
from io import BytesIO
import base64

import altair as alt
import pandas as pd


def create_sentiment_distribution_chart(df):
    """Creates a distribution graph of average score by topic and source."""
    color_scale = alt.Scale(domain=['Fox News', 'Democracy Now!'],
                            range=['red', 'blue'])

    points = alt.Chart(df).mark_circle().encode(
        x=alt.X('avg_polarity_score:Q', title="Average Polarity Score"),
        y=alt.Y('topic_name:O', title="Topic"),
        color=alt.Color('source_name:N', title="News Source",
                        scale=color_scale),
        tooltip=[alt.Tooltip(field="topic_name", title="Topic"),
                 alt.Tooltip(field="avg_polarity_score",
                             title="Average polarity score"),
                 alt.Tooltip(field="source_name", title="News Source")]
    ).properties(
        width=400,
        height=300
    ).interactive()
    vertical_line = alt.Chart(pd.DataFrame({'x': [0]})).mark_rule(color='black').encode(
        x='x:Q'
    )
    chart = alt.layer(points, vertical_line)

    return chart_to_base64(chart)


def create_bar_graph(df):
    """Creates a bar chart of sentiment scores with alternating bars for sources."""
    color_scale = alt.Scale(domain=['Fox News', 'Democracy Now!'],
                            range=['red', 'blue'])
    bars = alt.Chart(df).mark_bar(opacity=0.8).encode(
        x=alt.X('avg_polarity_score:Q',
                title='Average Polarity Score',
                axis=alt.Axis(grid=False),
                stack=None),
        y=alt.Y('topic_name:O', title='Topic', axis=alt.Axis(labelPadding=10)),
        color=alt.Color('source_name:N', scale=color_scale,
                        title='News Source'),
        tooltip=[alt.Tooltip(field="topic_name", title="Topic"),
                 alt.Tooltip(field="avg_polarity_score",
                             title="Average Polarity Score"),
                 alt.Tooltip(field="source_name", title="News Source")]
    ).properties(
        width=400,
        height=300
    ).interactive()
    vertical_line = alt.Chart(pd.DataFrame({'x': [0]})).mark_rule(color='black').encode(
        x='x:Q'
    )
    chart = alt.layer(bars, vertical_line).configure_axis(
        grid=False
    ).configure_view(
        strokeWidth=0
    )

    return chart_to_base64(chart)


def chart_to_base64(chart):
    """Converts chart to base64 image so can be emailed."""
    chart_image = BytesIO()
    chart.save(chart_image, format='png')
    chart_image.seek(0)
    base64_img = base64.b64encode(chart_image.read()).decode('utf-8')
    return base64_img
