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

## Usage

### Running the Extraction Process

Run the extraction process through the command `python3 extract_fn.py`


### Running the Cleaning Process

Run the cleaning process through the command `python3 clean_fn.py`