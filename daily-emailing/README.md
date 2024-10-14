
# Daily Media Sentiment Email Report

## Overview
This project automates the sending of daily email reports with a summary of media sentiment from various sources. It retrieves articles published the previous day, calculates the average polarity score by topic and source, and sends a styled HTML email to subscribers.

The project consists of scripts to:
- Interact with a PostgreSQL database.
- Generate an HTML report based on sentiment analysis.
- Send emails using AWS SES.
- Deploy the functionality using Docker and AWS Lambda.

## Prerequisites
Before running the project, ensure you have the following set up:
1. **Python 3.8+**: Required to run the scripts.
2. **PostgreSQL Database**: The project interacts with a PostgreSQL database to fetch article and sentiment data.
3. **AWS SES**: Amazon Simple Email Service (SES) is used for sending emails.
4. **Docker**: To build and deploy the project as a container.
5. **AWS ECR**: The project is pushed to an AWS Elastic Container Registry (ECR).

## Folder Structure

- `daily_email.py`: Script to send a daily email report
- `d_db_funcs.py`: Database interaction functions
- `html_content.py`: HTML generation for the email content
- `dockerise.sh`: Shell script to build and push Docker image
- `Dockerfile`: Docker configuration for deployment
- `requirements.txt`: Python dependencies
- `.env`: Environment variables (not included in version control)

## Set-up: Environmental variables

Create a `.env` file with the following environment variables:
```
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=your_database_port

AWS_ACCESS_KEY_BOUDICCA=your_aws_access_key
AWS_ACCESS_SECRET_KEY_BOUDICCA=your_aws_secret_key
FROM_EMAIL=your_ses_verified_email
ECR_REGISTRY_ID=your_ecr_registry_id
ECR_REPO_NAME=your_ecr_repo_name
IMAGE_NAME=your_docker_image_name
```

## Running Locally

1. Create a virtual environment.
2. Install the required dependencies with:
```
pip install -r requirements.txt
```
3. Run the script with:
```
python3 daily_email.py
```


## Deployment

To deploy this project to the cloud using Docker and AWS Lambda run this command:
```
bash dockerise.sh
```

