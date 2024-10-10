# Democracy Now News Scraper

## Overview

This module is responsible (at present) for extracting articles from various democracy now web pages and cleaning the extracted content. The extraction process involves:
    1. scraping all topics in https://www.democracynow.org/topics/browse, 
    2. retrieving all article links for each topic, filtering for those no older than 3 days, 
    3. extracting article content, and then cleaning the text to remove unwanted characters, stopwords, and trailing whitespace.

## Setup

1. Create a virtual environment:
    ```bash
    python3 -m venv venv
    ```
2. Activate the virtual environment.
    ```bash
    source venv/bin/activate
    ```
3. Install the required packages.
    ```bash
    pip install -r requirements.txt
    ```
4. Configure your environment `.env` file with the following variables:
    ```sh 
    AWS_ACCESS_KEY_BOUDICCA="your-aws-access-key"
    AWS_ACCESS_SECRET_KEY_BOUDICCA="your-aws-secret-access-key"

    S3_BUCKET_NAME="your-aws-s3-bucket-name"

    ECR_REGISTRY_ID="your-ecr-registry-id"
    ECR_REPO_NAME="your-ecr-repo-name-for-democracy-now-scraper"
    IMAGE_NAME="your-democracy-now-scraper-image-name"
    ```

5. Dockerising and Pushing to ECR Repository:

    ```sh
    bash dockerise.sh
    ```

## Files

- `extract_dn.py`: This file handles the extraction of articles from Democracy Now web pages. It uses `BeautifulSoup` to scrape the full content of the articles.

- `transform_dn.py`: Contains function to combine the results into a pandas dataframe.

- `load_dn.py`: Uploads the dataframe as a CSV to teh S3 bucket.

- `pipeline_dn.py`: This file contains the main Lambda handler function for the Democracy News scraper.

## Usage

### Running the Entire Pipeline Locally

To run the entire process (fetching, cleaning, and uploading to S3), execute the following command:

```sh
python3 pipeline_fn.py
```
