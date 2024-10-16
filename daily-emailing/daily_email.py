"""A script to send a html email of the previous days articles."""

from os import environ as ENV
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
import boto3

from html_content import generate_html
from d_db_funcs import (get_avg_polarity_by_topic_and_source_yesterday,
                        get_daily_subscribers, get_yesterday_date)


def get_ses_client() -> boto3.client:
    """Return boto3 ses client to send emails with"""

    return boto3.client("ses", region_name="eu-west-2",
                        aws_access_key_id=ENV["AWS_ACCESS_KEY_BOUDICCA"],
                        aws_secret_access_key=ENV["AWS_ACCESS_SECRET_KEY_BOUDICCA"])


def send_email() -> None:
    """Sends an email"""

    load_dotenv()
    emails = get_daily_subscribers()
    df = get_avg_polarity_by_topic_and_source_yesterday()
    html = generate_html(df)
    yesterday = get_yesterday_date()

    client = get_ses_client()
    message = MIMEMultipart()

    message["Subject"] = f"Media Sentiment Report for {yesterday}"
    body = MIMEText(html, "html")
    message.attach(body)

    client.send_raw_email(
        Source=ENV['FROM_EMAIL'],
        Destinations=emails,
        RawMessage={
            'Data': message.as_string()
        }
    )
    print("sent email")


def lambda_handler(event: dict, context: dict) -> dict:  # pylint: disable=W0613
    """AWS Lambda handler function."""

    try:
        send_email()
        print("Daily emails sent!")
        return {
            "statusCode": 200,
            "body": "Daily emails sent."
        }

    except Exception as e:  # pylint: disable=W0718
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }


if __name__ == "__main__":
    lambda_handler({}, {})
