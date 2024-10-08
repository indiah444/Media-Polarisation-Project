"""Combines JSON inputs from various scrapers and saves to S3 as CSV"""

import json
from io import StringIO
from os import environ as ENV
from datetime import datetime

import boto3
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
s3_client = boto3.client(service_name="s3",
                         aws_access_key_id=ENV["AWS_ACCESS_KEY_BOUDICCA"],
                         aws_secret_access_key=ENV["AWS_ACCESS_SECRET_KEY_BOUDICCA"])


def lambda_handler(event, context):
    """
    Combines JSON inputs from the event, saves the result as a CSV in S3 bucket.
    """

    combined_data = []

    for result in event:
        for key, value in result.items():
            body = json.loads(value['body'])
            body['source'] = key

            combined_data.append(body['data'])

    df = pd.DataFrame(combined_data)

    if not df.empty:
        save_to_s3(df, ENV['S3_BUCKET_NAME'])

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Data saved to S3", "combined_data": combined_data})
    }


def save_to_s3(dataframe: pd.DataFrame, bucket_name: str):
    """
    Saves a DataFrame to an S3 bucket as a CSV file with the current date and time as the filename.
    """

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_key = f"combined_data_{current_time}.csv"

    csv_buffer = StringIO()
    dataframe.to_csv(csv_buffer, index=False)

    s3_client.put_object(Bucket=bucket_name, Key=file_key,
                         Body=csv_buffer.getvalue())

    print(f"File saved to S3 with key: {file_key}")
