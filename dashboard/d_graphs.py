# pylint: disable=R0801

"""Script to create altair graphs for dashboard."""

import pandas as pd
import altair as alt
import streamlit as st

WEEKDAY_ORDER = ['Monday', 'Tuesday', 'Wednesday',
                 'Thursday', 'Friday', 'Saturday', 'Sunday']


@st.cache_data
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


@st.cache_data
def create_horizontal_line():
    """Returns horizontal line at y=0
    to clearly show where the x axis is"""

    return alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(
        color='black').encode(y='y:Q')


@st.cache_data
def create_vertical_line():
    """Returns vertical line at x=0
    to clearly show where y axis is"""

    return alt.Chart(pd.DataFrame({'x': [0]})).mark_rule(
        color='black').encode(x='x:Q')


@st.cache_data
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

    zero_line = create_horizontal_line() + create_vertical_line()

    final_chart = zero_line + scatter_chart

    final_chart = final_chart.configure_axis(
        grid=True).configure_view(stroke=None)

    return final_chart


@st.cache_data
def get_last_point(df: pd.DataFrame) -> pd.DataFrame:
    """Returns a dataframe with the maximum date published for each source."""

    last_point_df = df.dropna(subset=['date_published']).groupby('source_name').agg({
        'topic_name': 'last',
        'date_published': 'max',
        'title_polarity_score': 'last',
        'content_polarity_score': 'last'
    }).reset_index()

    return last_point_df


@st.cache_data
def visualise_change_over_time(df: pd.DataFrame, by_title: bool) -> alt.Chart:
    """Visualise changes in sentiment over time. """

    base = alt.Chart(df).encode(
        alt.Color("source_name:N", title='Source Name').legend(None)
    ).properties(
        width=500
    ).interactive()
    color_scale = alt.Scale(domain=['Fox News', 'Democracy Now!'],
                            range=['red', 'blue'])
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
        color=alt.Color('source_name:N', scale=color_scale)
    )

    source_names = points.mark_text(
        align="left", dx=10).encode(text="source_name")

    return line + points + source_names


@st.cache_data
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

    chart = alt.layer(points, create_vertical_line())

    return chart


@st.cache_data
def pivot_df(df: pd.DataFrame) -> pd.DataFrame:
    """Pivots dataframe so topics are rows and sources are columns."""

    pivoted_df = df.pivot(index='topic_name', columns='source_name',
                          values='avg_polarity_score').fillna('N/A')
    return pivoted_df


@st.cache_data
def add_source_columns(df: pd.DataFrame) -> str:
    """Add the source names as column titles."""

    color_scheme = {'Fox News': 'red', 'Democracy Now!': 'blue'}
    html = ""
    for source in df.columns:
        html += ("<th style='background-color: white; color:"
                 f"{color_scheme[source]};'>{source}</th>")
    return html


@st.cache_data
def add_topic_rows(df: pd.DataFrame) -> str:
    """Build the rows of the table with topic and score, with color based on score."""

    html = ""
    for topic, row in df.iterrows():
        html += ("<tr><td style='background-color: white; color: "
                 f"black;'>{topic}</td>")
        for score in row:
            if isinstance(score, float):
                color = "#fabbb7" if score < -0.5 else "#b6f7ae" if score > 0.5 else "#fafafa"

                html += (f"<td style='background-color: {color}; "
                         f"color: black;'>{score:.2f}</td>")
            else:
                html += ("<td style='background-color: white; "
                         f"color: black;'>{score}</td>")
        html += "</tr>"
    return html


@st.cache_data
def generate_html(df: pd.DataFrame) -> str:
    """Generate html body"""

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
    html += """
    <body>
        <table>
            <thead>
                <tr>
                    <th style='background-color: white; color: black'>Topic</th>
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


def visualise_heatmap(data_df: pd.DataFrame, by_title: bool,
                      colourscheme: str = 'yellowgreen') -> alt.Chart:
    """Returns an altair heatmap"""

    vals = "title_polarity_score" if by_title else "content_polarity_score"
    data_df = data_df[["week_num", "weekday", vals, "week_text", "date_name"]]

    data_df = data_df.groupby(["week_num", "week_text", "weekday", "date_name"],
                              as_index=False)[vals].mean()

    return alt.Chart(data_df).mark_rect().encode(
        x=alt.X('week_text:O', title='Week', sort=alt.EncodingSortField(
            field='week_num', order='ascending')),
        y=alt.Y('weekday:O', title='Day of the Week',  sort=WEEKDAY_ORDER),
        color=alt.Color(f'{vals}:Q', title='Polarity Score',
                        scale=alt.Scale(scheme=colourscheme, domain=[-1, 1])),
        tooltip=[alt.Tooltip(field=vals, title="Average Polarity Score"),
                 alt.Tooltip(field='date_name', title="Date")]
    ).properties(
        width=600,
        height=300
    )
