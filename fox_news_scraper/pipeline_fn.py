"""File that holds the main lambda handler function for the Fox News scraper."""

from dotenv import load_dotenv

from load_csv_fn import process_rss_feeds_and_upload

RSS_FEED_URLS = [
    "https://moxie.foxnews.com/google-publisher/latest.xml",
    "https://moxie.foxnews.com/google-publisher/world.xml",
    "https://moxie.foxnews.com/google-publisher/politics.xml",
    "https://moxie.foxnews.com/google-publisher/science.xml",
    "https://moxie.foxnews.com/google-publisher/health.xml",
    "https://moxie.foxnews.com/google-publisher/sports.xml",
    "https://moxie.foxnews.com/google-publisher/travel.xml",
    "https://moxie.foxnews.com/google-publisher/tech.xml",
    "https://moxie.foxnews.com/google-publisher/opinion.xml"
]


def lambda_handler(event, context):  # pylint: disable=W0613
    """AWS Lambda handler function."""

    try:
        process_rss_feeds_and_upload(RSS_FEED_URLS)
        return {
            "statusCode": 200,
            "body": "RSS feed data processed and uploaded to S3 successfully."
        }

    except Exception as e:  # pylint: disable=W0718
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }


if __name__ == "__main__":

    load_dotenv()

    result = lambda_handler({}, {})
    print(result)
