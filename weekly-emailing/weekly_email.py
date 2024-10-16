"""A script to send an email with a pdf of the previous weeks articles."""

from os import environ as ENV
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

from dotenv import load_dotenv
import boto3

from pdf_content import generate_pdf
from w_db_funcs import get_avg_polarity_last_week, get_weekly_subscribers


def get_ses_client() -> boto3.client:
    """Return boto3 ses client to send emails with"""

    return boto3.client("ses", region_name="eu-west-2",
                        aws_access_key_id=ENV["AWS_ACCESS_KEY_BOUDICCA"],
                        aws_secret_access_key=ENV["AWS_ACCESS_SECRET_KEY_BOUDICCA"])


def send_email() -> None:
    """Sends an email"""

    load_dotenv()
    emails = get_weekly_subscribers()
    df = get_avg_polarity_last_week()
    pdf_content = generate_pdf(df)

    client = get_ses_client()

    message = MIMEMultipart()

    message["Subject"] = "Media Sentiment Report for Last Week"
    body = MIMEText(
        "Dear subscriber, please find attached your weekly media sentiment report.",
        "plain")
    message.attach(body)

    attachment = MIMEApplication(pdf_content.read())
    attachment.add_header('Content-Disposition',
                          'attachment', filename='Weekly_sentiment_report.pdf')
    message.attach(attachment)

    client.send_raw_email(Source=ENV['FROM_EMAIL'],
                          Destinations=emails,
                          RawMessage={'Data': message.as_string()})
    print("sent email")


def lambda_handler(event: dict, context: dict) -> dict:  # pylint: disable=W0613
    """AWS Lambda handler function."""

    try:
        send_email()
        print("Weekly emails sent!")
        return {
            "statusCode": 200,
            "body": "Weekly emails sent."
        }

    except Exception as e:  # pylint: disable=W0718
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }


if __name__ == "__main__":
    lambda_handler({}, {})
