# Fox News Scraper

## Overview

This module is responsible (at present) for extracting articles from various Fox News RSS feeds and cleaning the extracted content. The extraction process involves fetching the RSS feed data, retrieving the full article content, and then cleaning the text to remove unwanted characters, stopwords, and trailing whitespace.

## Setup

1. `python3 -m venv venv` to create a virtual environment.
2. `source venv/bin/activate` to activate the virtual environment.
3. `pip install -r requirements.txt` to install the required packages.
4. Configure your environment `.env` file with the following variables:

```sh 
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

## Usage

### Running the Entire Pipeline

To run the entire process (fetching, cleaning, and uploading to S3), execute the following command:

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