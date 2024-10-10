"""The full pipeline for extracting articles, analysing them and uploading them to s3."""
from extract_s3 import extract
from transform_articles import transform
from load_rds import load


def pipeline() -> None:
    """The full elt pipeline."""
    articles = extract()
    articles = transform(articles)
    load(articles)


if __name__ == "__main__":
    pipeline()
