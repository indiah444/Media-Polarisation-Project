"""Script to generate the pdf report."""

from io import BytesIO

import pandas as pd
from xhtml2pdf import pisa

from graphs import create_bar_graph, create_sentiment_distribution_chart


def generate_html_report(df: pd.DataFrame) -> str:
    """Returns the contents as html."""

    avg_polarity_chart_img = create_bar_graph(df)
    sentiment_dist_chart_img = create_sentiment_distribution_chart(df)
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
            }}
            th, td {{
                padding: 8px;
                text-align: left;
                border-bottom: 1px solid #ddd;
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
        <h2>Average Polarity Scores by Topic and Source</h2>
        <img src="data:image/png;base64,{avg_polarity_chart_img}" alt="Average Polarity Chart">
        <h2>Sentiment Distribution</h2>
        <img src="data:image/png;base64,{sentiment_dist_chart_img}" \
alt="Sentiment Distribution Chart">
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
