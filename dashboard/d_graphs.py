"""Script to create altair graphs for dashboard."""

import pandas as pd
import altair as alt


def create_bubble_chart(df: pd.DataFrame) -> alt.Chart:
    """Returns a bubble chart of sentiment for a source by topic."""

    color_scale = alt.Scale(domain=['Fox News', 'Democracy Now!'],
                            range=['red', 'blue'])
    chart = alt.Chart(df).mark_circle().encode(
        x=alt.X('source_name:N', title='Source'),
        y=alt.Y('avg_polarity_score:Q',
                title='Average Polarity Score'),
        size=alt.Size('article_count:Q', title='Number of Articles'),
        color=alt.Color('source_name:N', title='Source', scale=color_scale),
        tooltip=[alt.Tooltip(field="article_count", title="Article count"),
                 alt.Tooltip(field="avg_polarity_score",
                             title="Average polarity score"),
                 alt.Tooltip(field="source_name", title="News Source")]
    ).properties(
        width=800,
        height=400
    )
    return chart


def create_scatter_graph(df: pd.DataFrame) -> alt.Chart:
    """Returns a scatter graph for title vs content score."""
    color_scale = alt.Scale(domain=['Fox News', 'Democracy Now!'],
                            range=['red', 'blue'])
    scatter_chart = alt.Chart(df).mark_point(filled=True).encode(
        x=alt.X('title_polarity_score:Q',
                scale=alt.Scale(domain=[-1.1, 1.1]),
                axis=alt.Axis(title='Title Polarity Score', grid=True)),
        y=alt.Y('content_polarity_score:Q',
                scale=alt.Scale(domain=[-1.1, 1.1]),
                axis=alt.Axis(title='Content Polarity Score', grid=True)),
        color=alt.Color('source_name:N', title='Source', scale=color_scale),
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

    final_chart = zero_line + scatter_chart

    final_chart = final_chart.configure_axis(
        grid=True
    ).configure_view(
        stroke=None
    )
    return final_chart


def create_sentiment_distribution_chart(df):
    """Creates a distribution graph of average score by topic and source."""
    color_scale = alt.Scale(domain=['Fox News', 'Democracy Now!'],
                            range=['red', 'blue'])

    points = alt.Chart(df).mark_circle().encode(
        x=alt.X('avg_polarity_score:Q', title="Average Polarity Score"),
        y=alt.Y('topic_name:O', title="Topic"),
        color=alt.Color('source_name:N', title="News Source",
                        scale=color_scale),
        size=alt.Size('article_count:Q', title='Number of Articles'),
        tooltip=[alt.Tooltip(field="topic_name", title="Topic"),
                 alt.Tooltip(field="avg_polarity_score",
                             title="Average polarity score"),
                 alt.Tooltip(field="source_name", title="News Source"),
                 alt.Tooltip(field="article_count", title="Article count")]
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

    return chart


def pivot_df(df: pd.DataFrame) -> pd.DataFrame:
    """Pivots dataframe so topics are rows and sources are columns."""
    pivoted_df = df.pivot(index='topic_name', columns='source_name',
                          values='avg_polarity_score').fillna('N/A')
    return pivoted_df


def add_source_columns(df: pd.DataFrame) -> str:
    """Add the source names as column titles."""
    color_scheme = {'Fox News': 'red', 'Democracy Now!': 'blue'}
    html = ""
    for source in df.columns:
        html += f"<th style='background-color: white; color: {color_scheme[source]};'>{source}</th>"
    return html


def add_topic_rows(df: pd.DataFrame) -> str:
    """Build the rows of the table with topic and score, with color based on score."""
    html = ""
    for topic, row in df.iterrows():
        html += f"<tr><td style='background-color: white;'>{topic}</td>"
        for score in row:
            if isinstance(score, float):
                color = "#fabbb7" if score < -0.5 else "#b6f7ae" if score > 0.5 else "#fafafa"
                html += f"<td style='background-color: {color};'>{score:.2f}</td>"
            else:
                html += f"<td style='background-color: white;'>{score}</td>"
        html += "</tr>"
    return html


def generate_html(df) -> str:
    score_df = pivot_df(df)
    html = """
    <html>
    <head>
        <style>
            table {
                font-family: Arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    """
    html += f"""
    <body>
        <table>
            <thead>
                <tr>
                    <th style='background-color: white;'>Topic</th>
    """
    html += add_source_columns(score_df)
    html += """
                </tr>
            </thead>
            <tbody>
    """
    html += add_topic_rows(score_df)
    html += """
            </tbody>
        </table>
    </body>
    </html>
    """

    return html
