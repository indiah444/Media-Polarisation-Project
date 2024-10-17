"""Script to generate the html content."""

from datetime import datetime, timedelta
from os import environ as ENV

import pandas as pd

from d_db_funcs import get_yesterday_links_and_titles


def pivot_df(df: pd.DataFrame) -> pd.DataFrame:
    """Pivots dataframe so topics are rows and sources are columns."""

    pivoted_df = df.pivot(index='topic_name', columns='source_name',
                          values='avg_polarity_score').fillna('N/A')
    return pivoted_df


def add_source_columns(df: pd.DataFrame) -> str:
    """Add the source names as column titles."""

    html = []
    for source in df.columns:
        html.append(f"<th style='background-color: white;'>{source}</th>")
    return "".join(html)


def add_topic_rows(df: pd.DataFrame) -> str:
    """Build the rows of the table with topic and score, with color based on score."""

    html = ""
    for topic, row in df.iterrows():
        html += f"<tr><td style='background-color: white;'>{topic}</td>"
        for score in row:
            if isinstance(score, float):
                color = "#fabbb7" if score < -0.5 else "#b6f7ae" if score > 0.5 else "#fafafa"
                html += \
                    f"<td style='background-color: {color};'>{score:.2f}</td>"
            else:
                html += f"<td style='background-color: white;'>{score}</td>"
        html += "</tr>"
    return html


def get_url_html(url: dict) -> str:
    """Returns a formatted string for a URL."""

    return f'<li><a href="{url['link']}">{url['title']}</a></li>'


def generate_html_with_links() -> str:
    """Creates a list of yesterdays articles urls."""

    urls = get_yesterday_links_and_titles()
    topics = sorted({row['topic'] for row in urls})
    html = "<h2>Yesterday's articles:</h2>"
    for topic in topics:
        html += f'<h4>{topic}</h4>\n<ul>\n'
        html += "".join([get_url_html(u) for u in urls if u['topic'] == topic])
        html += "</ul>"

    return html


def add_unsubscribe_link() -> str:
    """Adds the link to the unsubscribe page."""

    link = ENV['EC2_HOST'] + ":8501/Subscribe"
    return f'<a href="{link}" target="_blank">Unsubscribe here</a>'


def generate_html(df: pd.DataFrame) -> str:
    """Return HTML string to send in email body"""

    score_df = pivot_df(df)
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%d-%m-%Y')
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
        <h2>Average Content Polarity Score by Topic and Source \
(Published Yesterday - {yesterday})</h2>
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
        """
    html += generate_html_with_links()
    html += add_unsubscribe_link()
    html += """
    </body>
    </html>
    """

    return html


if __name__ == "__main__":
    print(generate_html_with_links())
