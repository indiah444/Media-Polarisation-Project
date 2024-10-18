"""Script to generate the pdf report."""

from io import BytesIO

import pandas as pd
from xhtml2pdf import pisa

from graphs import create_whisker_plot


def add_source_columns(df: pd.DataFrame) -> str:
    """Add the source names as column titles."""

    html = []
    for source in df.columns:
        html.append(f"<th style='background-color: white;'>{source}</th>")
    return ''.join(html)


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


def pivot_df(df: pd.DataFrame) -> pd.DataFrame:
    """Pivots dataframe so topics are rows and sources are columns."""

    pivoted_df = df.pivot(index='topic_name', columns='source_name',
                          values='avg_polarity_score').fillna('N/A')
    return pivoted_df


def generate_html_report(df: pd.DataFrame) -> str:
    """Returns the contents as html."""

    whisker_chat_img = create_whisker_plot(df)
    score_df = pivot_df(df)
    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
            }}
            h1 {{
                text-align: center;
                color: red;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                border: 1px solid black;
            }}
            th, td {{
                padding: 8px;
                text-align: left;
                border-bottom: 1px solid #ddd;
                border: 1px solid black;
            }}
            img {{
                display: block;
                margin-left: auto;
                margin-right: auto;
            }}
        </style>
    </head>
    <body>
        <h1>Weekly Polarity Report</h1>
        <h2>Average Polarity Scores by Topic and Source (Published Last Week</h2>
        <img src="data:image/png;base64,{whisker_chat_img}" alt="Average Polarity Chart">
        <h2>Average Content Polarity Score by Topic and Source (Published Last Week)</h2>
        <table>
            <thead>
                <tr>
                    <th style='background-color: white;'>Topic</th>
    """
    html_content += add_source_columns(score_df)
    html_content += """
                </tr>
            </thead>
            <tbody>
    """
    html_content += add_topic_rows(score_df)
    html_content += """
            </tbody>
        </table>
        """

    html_content += """
        <p>Data is based on articles published over the past week.</p>
    </body>
    </html>
    """

    return html_content


def generate_pdf(df: pd.DataFrame) -> BytesIO:
    """Converts the html to a pdf."""

    html_content = generate_html_report(df)
    pdf_buffer = BytesIO()
    pisa.CreatePDF(html_content, dest=pdf_buffer)
    pdf_buffer.seek(0)

    return pdf_buffer
