"""Extracts the csv from s3 bucket and returns as dataframe."""
from io import BytesIO
from os import environ as ENV
from datetime import datetime, timedelta, timezone

from boto3 import client
import pandas as pd
from dotenv import load_dotenv


def get_object_names(s3_client: client, bucket_name: str) -> list[str]:
    """Returns a list of object names for a specific bucket, at a specific time."""
    objects = s3_client.list_objects(Bucket=bucket_name)
    now = datetime.now(timezone.utc)
    one_hour_ago = now - timedelta(hours=48)

    object_names = [o["Key"] for o in objects.get(
        "Contents", []) if o["LastModified"] >= one_hour_ago and o["Key"].endswith(
            "_article_data.csv")]
    if len(object_names) == 0:
        raise ValueError("No csvs in S3 bucket to upload.")
    return object_names


def create_dataframe(s3_client: client, bucket_name: str, file_name: str) -> pd.DataFrame:
    """Returns the object as a dataframe."""
    current_bytes = BytesIO()
    s3_client.download_fileobj(
        Bucket=bucket_name, Key=file_name, Fileobj=current_bytes)
    current_bytes.seek(0)
    current_df = pd.read_csv(current_bytes)

    return current_df


def delete_object(s3_client: client, bucket_name: str, file_name: str) -> None:
    """Deletes the file from the s3 bucket."""
    s3_client.delete_object(
        Bucket=bucket_name, Key=file_name
    )


def extract() -> pd.DataFrame:
    """Extracts the most recent files and returns a dataframe."""
    load_dotenv()
    bucket_name = ENV['BUCKET_NAME']
    s3 = client(service_name="s3",
                aws_access_key_id=ENV["AWS_ACCESS_KEY"],
                aws_secret_access_key=ENV["AWS_SECRET_KEY"])

    names = get_object_names(s3, bucket_name)
    all_dfs = []
    for name in names:
        all_dfs.append(create_dataframe(s3, bucket_name, name))
        delete_object(s3, bucket_name, name)
    if len(all_dfs) == 0:
        raise ValueError("No dataframes where found.")
    final_df = pd.concat(all_dfs, ignore_index=True)

    return final_df


if __name__ == "__main__":
    print(extract())
