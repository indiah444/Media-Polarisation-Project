# <img src="../assets/DN_logo.png" alt="Fox" width="50" height="50"> Democracy Now News Scraper

## 📋 Overview

This module is responsible (at present) for extracting articles from various democracy now web pages and cleaning the extracted content. The extraction process involves:
    1. Scraping all topics in https://www.democracynow.org/topics/browse
    2. Retrieving all article links for each topic, filtering for those no older than 3 days
    3. Extracting article title and content
    4. Cleaning the text to remove unwanted characters and trailing whitespace
    5. Transforming the data into a dataframe and loading as a CSV into the correct S3 bucket.

## 🛠️ Prerequisites
- **Docker** installed.
- Setup **ECR** repository to store Democracy Now scraper docker image.  

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
- `extract_dn.py`: This file handles the extraction of articles from Democracy Now web pages. It uses `BeautifulSoup` to scrape the full content of the articles.
- `transform_dn.py`: Contains function to combine the results into a pandas dataframe.
- `load_dn.py`: Uploads the dataframe as a CSV to the S3 bucket.
- `pipeline_dn.py`: This file contains the main Lambda handler function that runs the ETL pipeline for the Democracy News scraper.

### ✅ Test coverage
To generate a detailed test report:
```bash
pytest -vv
```
To include coverage results:
```bash
pytest --cov -vv
```