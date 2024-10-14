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
        tooltip=[alt.Tooltip(field="article_count", title="Article count"),
                 alt.Tooltip(field="avg_polarity_score",
                             title="Average polarity score"),
                 alt.Tooltip(field="source_name", title="News Source")]
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
        tooltip=[alt.Tooltip(field="article_title", title="Article title"),
                 alt.Tooltip(field="title_polarity_score",
                             title="Title polarity score"),
                 alt.Tooltip(field="content_polarity_score",
                             title="Content polarity score"),
                 alt.Tooltip(field="source_name", title="News Source")]
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


def create_sentiment_distribution_chart(df):
    """Creates a distribution graph of average score by topic and source."""
    df['article_count'] = df.groupby(['topic_name', 'source_name'])[
        'avg_polarity_score'].transform('count')
    color_scale = alt.Scale(domain=['Fox News', 'Democracy Now!'],
                            range=['red', 'blue'])

    points = alt.Chart(df).mark_circle().encode(
        x=alt.X('avg_polarity_score:Q', title="Average Polarity Score"),
        y=alt.Y('topic_name:O', title="Topic"),
        color=alt.Color('source_name:N', title="News Source",
                        scale=color_scale),
        size=alt.Size('article_count:Q', legend=None, scale=alt.Scale(
            range=[30, 300])),
        tooltip=[alt.Tooltip(field="topic_name", title="Topic"),
                 alt.Tooltip(field="avg_polarity_score",
                             title="Average polarity score"),
                 alt.Tooltip(field="article_count",
                             title="Article count"),
                 alt.Tooltip(field="source_name", title="News Source")]
    ).properties(
        width=400,
        height=300
    ).interactive()
    vertical_line = alt.Chart(pd.DataFrame({'x': [0]})).mark_rule(color='black').encode(
        x='x:Q'
    )
    chart = alt.layer(points, vertical_line)

    return chart


def create_bar_graph_of_topic_sentiment(df):
    """Creates a bar chart of scores.
    Need to fix"""
    base_chart = alt.Chart(df).properties(
        width=150,
        height=200
    )
    bars = base_chart.mark_bar().encode(
        x='avg_polarity_score:Q',
        y='topic_name:O',
        color='avg_polarity_score:Q',
        tooltip=[alt.Tooltip(field="topic_name", title="Topic"),
                 alt.Tooltip(field="avg_polarity_score",
                             title="Average polarity score"),
                 alt.Tooltip(field="source_name", title="News Source")]
    ).interactive()
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

    return faceted_chart
