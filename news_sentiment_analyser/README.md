# News Sentiment Analyser

## Overview

This module is responsible for assigning a sentiment score for the extracted articles, and grouping them into different topics. Sentiment analysis is performed using (VADER)[https://ojs.aaai.org/index.php/ICWSM/article/view/14550]. VADER is a rule-based sentiment analyser which can map the "intensity" and nature of emotions to a score. Passed to the database is a compound score for the `title` and `content`, normalised to lie in the range $[-1,1]$. As for topic labelling, we begin with a pre-set list. Articles are mapped to 0, 1 or more topics, depending on their title. This is handled using `gpt-4o-mini` OpenAI model.

- [ ] Possibly more detail here on topics

## Setup 

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

    OPENAI_API_KEY="your-openai-key"
    OPENAI_MODEL="your-openai-model"
    ```

5. Dockerising and Pushing to ECR Repository:

    ```sh
    bash dockerise.sh
    ```

6. Running the pipeline 

```sh
python3 pipeline_analysis.py
```

## Test coverage

## Methodology 


### OpenAI API


### Sentiment Analysis 


#### Further improvements 