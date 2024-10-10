from datetime import datetime

from dotenv import load_dotenv

from extract_dn import scrape_democracy_now
from transform_dn import convert_to_dataframe
from load_dn import upload_dataframe_to_s3


def lambda_handler(event: dict, context: dict) -> dict:
    """AWS Lambda handler function."""

    try:
        load_dotenv()

        results = scrape_democracy_now(days_old=3)
        if not results:
            print("No article data found")
            return

        df = convert_to_dataframe(results)
        if df is None:
            print("Could not convert results to dataframe")
            return

        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        s3_filename = f"{current_time}_democracy_now_article_data.csv"
        upload_dataframe_to_s3(df, s3_filename)

        return {
            "statusCode": 200,
            "body": "Data extracted, processed and uploaded to S3 successfully."
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }


if __name__ == '__main__':
    lambda_handler({}, {})
