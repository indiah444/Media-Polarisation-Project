"""A script to send a html email of the previous days articles."""
from os import environ as ENV
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from datetime import datetime, timedelta

from dotenv import load_dotenv
import boto3

from html_content import generate_html
from d_db_funcs import get_avg_polarity_by_topic_and_source_yesterday, get_daily_subscribers


def send_email() -> None:
    """Sends an email"""

    load_dotenv()
    emails = get_daily_subscribers()
    df = get_avg_polarity_by_topic_and_source_yesterday()
    html = generate_html(df)
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%d-%m-%Y')
    client = boto3.client("ses", region_name="eu-west-2",
                          aws_access_key_id=ENV["AWS_ACCESS_KEY_BOUDICCA"],
                          aws_secret_access_key=ENV["AWS_ACCESS_SECRET_KEY_BOUDICCA"])
    message = MIMEMultipart()

    message["Subject"] = f"Media Sentiment Report for {yesterday}"
    body = MIMEText(
        html,
        "html")
    message.attach(body)

    client.send_raw_email(
        Source='trainee.megan.lester@sigmalabs.co.uk',
        Destinations=emails,
        RawMessage={
            'Data': message.as_string()
        }
    )
    print("sent email")


if __name__ == "__main__":
    send_email()
