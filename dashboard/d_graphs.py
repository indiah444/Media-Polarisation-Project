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


def get_last_point(df: pd.DataFrame) -> pd.DataFrame:
    """Returns a dataframe with the maximum date published for each source."""
    last_point_df = df.dropna(subset=['date_published']).groupby('source_name').agg({
        'topic_name': 'last',
        'date_published': 'max',
        'title_polarity_score': 'last',
        'content_polarity_score': 'last'
    }).reset_index()

    return last_point_df


def visualise_change_over_time(df: pd.DataFrame, by_title: bool) -> alt.Chart:
    """Visualise changes in sentiment over time. """
    base = alt.Chart(df).encode(
        alt.Color("source_name:N", title='Source Name').legend(None)
    ).properties(
        width=500
    ).interactive()

    if not by_title:
        y_axis = ('content_polarity_score', "Content Polarity Score")
    else:
        y_axis = ('title_polarity_score', "Title Polarity Score")

    line = base.mark_line().encode(
        x=alt.X('date_published:T', axis=alt.Axis(
            offset=-150, title='Date Published', titleAnchor="end")),

        y=alt.Y(f'{y_axis[0]}:Q', title=y_axis[1]),

        tooltip=[
            alt.Tooltip(field="source_name", title="Source Name"),
            alt.Tooltip(field=f"{y_axis[0]}", title=f"Average {y_axis[1]}")
        ]
    ).properties(
        width=500).interactive()

    last_point = get_last_point(df).reset_index(drop=True)

    points = alt.Chart(last_point).mark_circle(size=100).encode(
        x='date_published:T',
        y=alt.Y(f'{y_axis[0]}:Q'),
        tooltip=[alt.Tooltip('source_name:N', title='Source Name')],
        color=alt.Color('source_name:N')
    )

    source_names = points.mark_text(
        align="left", dx=10).encode(text="source_name")

    return line + points + source_names
