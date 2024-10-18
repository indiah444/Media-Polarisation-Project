"""Script to create the graphs to be sent as an email."""

from io import BytesIO
import base64

import altair as alt
import pandas as pd


def chart_to_base64(chart) -> str:
    """Converts chart to base64 image so can be emailed."""

    chart_image = BytesIO()
    chart.save(chart_image, format='png')
    chart_image.seek(0)
    base64_img = base64.b64encode(chart_image.read()).decode('utf-8')
    return base64_img


def create_whisker_plot(df) -> str:
    """Creates a whisker plot-style chart of sentiment scores with 
    horizontal lines and end ticks for sources."""

    color_scale = alt.Scale(domain=['Fox News', 'Democracy Now!'],
                            range=['red', 'blue'])
    lines = alt.Chart(df).mark_rule(opacity=0.8).encode(
        x=alt.X('avg_polarity_score:Q',
                title='Average Polarity Score',
                axis=alt.Axis(grid=True)),
        y=alt.Y('topic_name:O', title='Topic'),
        color=alt.Color('source_name:N', scale=color_scale,
                        title='News Source'),
        tooltip=[alt.Tooltip(field="topic_name", title="Topic"),
                 alt.Tooltip(field="avg_polarity_score",
                             title="Average Polarity Score"),
                 alt.Tooltip(field="source_name", title="News Source")]
    )

    ticks = alt.Chart(df).mark_tick(
        opacity=0.8,
        thickness=2,
        size=20
    ).encode(
        x=alt.X('avg_polarity_score:Q'),
        y=alt.Y('topic_name:O'),
        color=alt.Color('source_name:N', scale=color_scale)
    )
    vertical_line = alt.Chart(pd.DataFrame({'x': [0]})).mark_rule(color='black').encode(
        x='x:Q'
    )
    chart = alt.layer(lines, ticks, vertical_line).configure_axis(
        grid=False
    ).configure_view(
        strokeWidth=0
    ).properties(
        width=400,
        height=300
    ).interactive()

    return chart_to_base64(chart)
