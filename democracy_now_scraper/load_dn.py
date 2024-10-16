"""Function to upload DataFrame object as CSV to S3 bucket."""

from os import environ as ENV
from io import StringIO

import pandas as pd
import boto3


def upload_dataframe_to_s3(df: pd.DataFrame, object_name: str) -> None:
    """Upload the DataFrame as a CSV file to an S3 bucket."""

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    s3_bucket = ENV['S3_BUCKET_NAME']
    s3_client = boto3.client(service_name="s3",
                             aws_access_key_id=ENV["AWS_ACCESS_KEY_BOUDICCA"],
                             aws_secret_access_key=ENV["AWS_ACCESS_SECRET_KEY_BOUDICCA"])
    s3_client.put_object(Bucket=s3_bucket, Key=object_name,
                         Body=csv_buffer.getvalue())

    print(f"Uploaded DataFrame to s3://{s3_bucket}/{object_name}")
