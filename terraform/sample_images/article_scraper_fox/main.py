"""Dummy ETL script for scraping of Fox news website"""

from datetime import datetime
from io import StringIO
import json
from os import environ as ENV


import boto3
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def lambda_handler(event, context):
    """Generate a dummy DataFrame and upload to S3"""

    data = {
        'Article Heading': ['Heading 1', 'Heading 2', 'Heading 3'],
        'Article Content': ['Content of article 1', 'Content of article 2', 'Content of article 3'],
        'Date Published': [datetime.now().strftime("%Y-%m-%d")] * 3
    }

    df = pd.DataFrame(data)

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    s3_key = f'{current_time}_fox_article_data.csv'
    s3_bucket = ENV['S3_BUCKET_NAME']
    s3_client = boto3.client(service_name="s3",
                             aws_access_key_id=ENV["AWS_ACCESS_KEY_BOUDICCA"],
                             aws_secret_access_key=ENV["AWS_ACCESS_SECRET_KEY_BOUDICCA"])
    s3_client.put_object(Bucket=s3_bucket, Key=s3_key,
                         Body=csv_buffer.getvalue())

    response = {
        "statusCode": 200,
        "body": json.dumps({
            "message": "DataFrame successfully uploaded to S3",
            "s3_bucket": s3_bucket,
            "s3_key": s3_key
        })
    }

    return response
