# pylint: disable=unused-import

"""
A file to convert the data extracted from the RSS feed 
into a CSV and load it into the S3 bucket.
"""

import grequests  # This must be here to avoid file version errors

from os import environ as ENV
from datetime import datetime
from io import StringIO

import pandas as pd
import boto3

from extract_fn import fetch_from_multiple_feeds


def combine_entries_to_dataframe(entries: list[dict]) -> pd.DataFrame:
    """Converts the list of article entries into a Pandas DataFrame."""

    df = pd.DataFrame(entries)
    return df


def upload_dataframe_to_s3(df: pd.DataFrame, bucket_name: str, s3_filename: str):
    """Uploads the DataDrame as a CSV to an S3 bucket using in-memory storage
    (i.e. StringIO)."""

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    s3_client = boto3.client(service_name="s3",
                             aws_access_key_id=ENV["AWS_ACCESS_KEY_BOUDICCA"],
                             aws_secret_access_key=ENV["AWS_ACCESS_SECRET_KEY_BOUDICCA"])
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_filename,
            Body=csv_buffer.getvalue()
        )
        print(f"File uploaded to S3 bucket '{bucket_name}' as '{s3_filename}'")

    except Exception as e:  # pylint: disable=W0718
        print(f"Failed to upload file to S3: {e}")


def process_rss_feeds_and_upload(feed_urls: list[str]):
    """Combines the fetching, cleaning, combining, and uploading of RSS data."""

    entries = fetch_from_multiple_feeds(feed_urls)

    df = combine_entries_to_dataframe(entries)
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    bucket_name = ENV["S3_BUCKET_NAME"]
    s3_filename = f"{current_time}_fox_news_article_data.csv"
    upload_dataframe_to_s3(df, bucket_name, s3_filename)
