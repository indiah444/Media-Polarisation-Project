"""Script to create altair graphs for dashboard."""

import pandas as pd
import altair as alt


def create_bubble_chart(df: pd.DataFrame) -> alt.Chart:
    """Returns a bubble chart of sentiment for a source by topic."""
    return alt.Chart(df).mark_circle().encode(
        x=alt.X('source_name:N', title='Source'),
        y=alt.Y('avg_polarity_score:Q',
                title='Average Polarity Score'),
        size=alt.Size('article_count:Q', title='Number of Articles'),
        color=alt.Color('source_name:N', title='Source'),
        tooltip=['source_name', 'avg_polarity_score', 'article_count']
    ).properties(
        width=800,
        height=400
    )


def create_scatter_graph(df: pd.DataFrame) -> alt.Chart:
    """Returns a scatter graph for title vs content score."""
    scatter_chart = alt.Chart(df).mark_point(filled=True).encode(
        x=alt.X('title_polarity_score:Q',
                scale=alt.Scale(domain=[-1, 1]),
                axis=alt.Axis(title='Title Polarity Score', grid=True)),
        y=alt.Y('content_polarity_score:Q',
                scale=alt.Scale(domain=[-1, 1]),
                axis=alt.Axis(title='Content Polarity Score', grid=True)),
        color=alt.Color('source_name:N', title='Source'),
        tooltip=['article_title', 'title_polarity_score',
                 'content_polarity_score', 'source_name']
    ).properties(
        width=800,
        height=400
    ).interactive()

    zero_line = alt.Chart(pd.DataFrame({'x': [0], 'y': [0]})).mark_rule(color='black').encode(
        x='x:Q'
    ) + alt.Chart(pd.DataFrame({'x': [0], 'y': [0]})).mark_rule(color='black').encode(
        y='y:Q'
    )

    final_chart = scatter_chart + zero_line

    final_chart = final_chart.configure_axis(
        grid=True
    ).configure_view(
        stroke=None
    )
    return final_chart
