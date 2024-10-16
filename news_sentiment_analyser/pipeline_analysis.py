"""The full pipeline for extracting articles, analysing them and uploading them to s3."""

from extract_s3 import extract
from transform_articles import transform
from load_rds import load


def pipeline() -> None:
    """The full elt pipeline."""
    try:
        articles = extract()
        print("Articles extracted!")
        articles = transform(articles)
        print("Articles transformed.")
        load(articles)
        print("Articles inserted.")
    except Exception as err:  # pylint: disable=W0718
        print(f"Error occurred: {err}")


if __name__ == "__main__":
    pipeline()
