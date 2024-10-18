# <img src="../assets/FN_logo.png" alt="Fox" width="50" height="50"> Fox News Scraper

## 📋 Overview

This module is responsible for extracting articles from various Fox News RSS feeds, cleaning the extracted content, and loading the final cleaned data. The extraction process involves:
1. Fetching the RSS feed data, retrieving the full article content
2. Transforming the data into a dataframe and loading as a CSV into the correct S3 bucket.

## 🛠️ Prerequisites
- **Docker** installed.
- Setup **ECR** repository to store Fox News scraper docker image.  

Optional:
- **Python** installed (For running locally)

## ⚙️ Setup
Create a `.env` file and fill with the following variables
```env
# AWS Configuration
AWS_ACCESS_KEY_BOUDICCA=<your_aws_access_key>
AWS_ACCESS_SECRET_KEY_BOUDICCA=<your_aws_secret_access_key>

# ECR Configuration
ECR_REGISTRY_ID=<id_of_ecr_repo_to_store_image>
ECR_REPO_NAME=<name_of_ecr_repo_to_store_image>
IMAGE_NAME=article-analyser-image  # or any other appropriate name

# S3 Bucket Configuration
S3_BUCKET_NAME=<s3_bucket_name>
```

### ☁️ Pushing to the Cloud
To deploy the overall cloud infrastructure the Fox News scraper must be containerised and hosted on the cloud:

1. Make sure you have the Docker application running in the background
2. Dockerise and upload the application:
    ```bash
    bash dockerise.sh
    ```
    This will:
    - Authenticate your aws credentials with docker
    - Create the docker image
    - Tag the docker image
    - Upload tagged image to the ECR repository

### 💻 Running Locally (MacOS, **Optional**)
The Fox News web scraper can also be ran locally by:

1. Creating and activating virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
2. Install requirements
    ```bash
    pip install -r requirements.txt
    ```
3. Run the entire process locally (fetching, cleaning, and uploading to S3):
    ```bash
    python3 pipeline_fn.py
    ```

## 📁 Files
- `extract_fn.py`: This file handles the extraction of articles from Fox News RSS feeds. It uses the `feedparser` library to parse RSS feeds and `BeautifulSoup` to scrape the full content of the articles.
- `load_fn.py`: This file converts the cleaned data into a Pandas DataFrame and uploads it as a CSV to an S3 bucket. It combines the fetching, cleaning, and uploaded processes.
- `pipeline_fn.py`: This file contains the main Lambda handler function for the Fox News scraper. It orchestrates the entire flow from fetching data from RSS feeds to uploading the processed data to S3.
- `Dockerfile`: This file is dockerises `pipeline_fn.py` so that it can be run on the cloud.

### ✅ Test coverage
To generate a detailed test report:
```bash
pytest -vv
```
To include coverage results:
```bash
pytest --cov -vv
```