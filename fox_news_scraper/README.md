# Fox News Scraper

## Overview

This module is responsible for extracting articles from various Fox News RSS feeds, cleaning the extracted content, and loading the final cleaned data. The extraction process involves fetching the RSS feed data, retrieving the full article content, and then cleaning the text to remove unwanted characters, stopwords, and trailing whitespace. The cleaned data is then transformed into a CSV and loaded into the correct S3 bucket.

## Setup

1. `python3 -m venv venv` to create a virtual environment.
2. `source venv/bin/activate` to activate the virtual environment.
3. `pip install -r requirements.txt` to install the required packages.
4. Configure your environment `.env` file with the following variables:

```sh 
AWS_ACCESS_KEY_BOUDICCA=XXXXXX
AWS_ACCESS_SECRET_KEY_BOUDICCA=XXXXXX
DB_HOST=XXXXXX
DB_PORT=XXXXX
DB_PASSWORD=XXXXXX
DB_USER=XXXXX
DB_NAME=XXXXX
```

## Files

- `extract_fn.py`: This file handles the extraction of articles from Fox News RSS feeds. It uses the `feedparser` library to parse RSS feeds and `BeautifulSoup` to scrape the full content of the articles.

- `clean_fn.py`: This file cleans the extracted article content by removing URLs, punctuation, and stopwords using regular expressions and NLTK's stopword corpus.

- `load_fn.py`: This file converts the cleaned data into a Pandas DataFrame and uploads it as a CSV to an S3 bucket. It combines the fetching, cleaning, and uploaded processes.

- `pipeline_fn.py`: This file contains the main Lambda handler function for the Fox News scraper. It orchestrates the entire flow from fetching data from RSS feeds to uploading the processed data to S3.

- `Dockerfile`: This file is dockerises `pipeline_fn.py` so that it can be run on the cloud.

## Usage

### Running the Entire Pipeline

To run the entire process locally (fetching, cleaning, and uploading to S3), execute the following command:

```sh
python3 pipeline_fn.py
```

### Running the Extraction Process

If you want to run the extraction process separately, you can execute:

```sh
python3 extract_fn.py
```


### Running the Cleaning Process

To run the cleaning process separately, you can execute:

```sh
python3 clean_fn.py
```

### Docker Setup

To build the Docker image, run the following command from the project directory:

```sh
docker build -t c13-boudicca-mp-fox-news-scraper . --platform "linux/amd64"
```

Once built, the Docker image can be pushed to an ECR repository named `c13-boudicca-mp-fox-news-scraper`. To push it, run the following commands:

```sh
aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 129033205317.dkr.ecr.eu-west-2.amazonaws.com

docker tag c13-boudicca-mp-fox-news-scraper:latest 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c13-boudicca-mp-fox-news-scraper:latest

docker push 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c13-boudicca-mp-fox-news-scraper:latest
```