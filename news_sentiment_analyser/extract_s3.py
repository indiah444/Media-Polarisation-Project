"""Extracts the csv from s3 bucket and returns as dataframe."""
from io import BytesIO
from os import environ as ENV

from boto3 import client
import pandas as pd
from dotenv import load_dotenv


def get_object_name(s3_client, bucket_name: str) -> str:
    """Returns a list of object names for a specific bucket, at a specific time."""

    objects = s3_client.list_objects(Bucket=bucket_name)

    return [o["Key"] for o in objects["Contents"]][0]


def create_dataframe(s3_client, bucket_name: str, file_name: str) -> pd.DataFrame:
    """Returns the object as a dataframe."""
    current_bytes = BytesIO()
    s3_client.download_fileobj(
        Bucket=bucket_name, Key=file_name, Fileobj=current_bytes)
    current_bytes.seek(0)
    current_df = pd.read_csv(current_bytes)
    return current_df


def delete_object(s3_client, bucket_name: str, file_name: str) -> None:
    """Deletes the file from the s3 bucket."""
    s3_client.delete_object(
        Bucket=bucket_name, Key=file_name
    )


def extract():
    """Extracts the most recent files and returns a dataframe."""
    bucket_name = ENV['BUCKET_NAME']

    s3 = client(service_name="s3",
                aws_access_key_id=ENV["AWS_ACCESS_KEY"],
                aws_secret_access_key=ENV["AWS_SECRET_ACCESS_KEY"])

    name = get_object_name(s3, bucket_name)
    df = create_dataframe(s3, bucket_name, name)
    delete_object(s3, bucket_name, name)
    print("Data extracted from s3.")
    return df


if __name__ == "__main__":
    pass
