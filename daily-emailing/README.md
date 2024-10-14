
# 🕘 ✉️ Daily Media Sentiment Email Report

## 📋 Overview
This project automates the sending of daily email reports with a summary of media sentiment from various sources. It retrieves articles published the previous day, calculates the average polarity score by topic and source, and sends a styled HTML email to subscribers.

The project consists of scripts to:
- Interact with a PostgreSQL database.
- Generate an HTML report based on sentiment analysis.
- Send emails using AWS SES.
- Deploy the functionality using Docker and AWS Lambda.

## 🛠️ Prerequisites
Before running the project, ensure you have the following set up:
4. **Docker** installed.
5. **AWS ECR** repository to store daily email generator docker image
5. Access to **AWS SES**: Amazon Simple Email Service (SES) is called within the scripts and is used for sending emails.

Optional:
- **Python** installed (For running scripts locally)

## ⚙️ Set-up: Environmental variables

1. Create a `.env` file with the following environment variables:
    ```
    # AWS Configuration
    AWS_ACCESS_KEY_BOUDICCA=<your_aws_access_key>
    AWS_ACCESS_SECRET_KEY_BOUDICCA=<your_aws_secret_access_key>

    # Database Configuration
    DB_HOST=<database_host_address>
    DB_PORT=<database_port>
    DB_PASSWORD=<database_password>
    DB_USER=<database_user>
    DB_NAME=<database_name>

    # S3 Bucket Configuration
    BUCKET_NAME=<s3_bucket_name>

    # ECR Configuration
    ECR_REGISTRY_ID=<id_of_ecr_repo_to_store_image>
    ECR_REPO_NAME=<name_of_ecr_repo_to_store_image>
    IMAGE_NAME=daily-email-image  # or any other appropriate name

    # Email Configuration
    FROM_EMAIL=your_ses_verified_email
    ```

### ☁️ Pushing to the Cloud
To deploy the overall cloud infrastructure, the daily email generator must be containerised and hosted on the cloud:

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

### 💻 Running Locally (MacOS)
The daily email generator can also be ran locally by:

1. Creating and activating virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
2. Install requirements
    ```bash
    pip install -r requirements.txt
    ```
3. Running the pipeline:
    ```bash
    python3 daily_email.py.py
    ```
```

## 📁 Files

- `daily_email.py`: Script to send a daily email report
- `d_db_funcs.py`: Database interaction functions
- `html_content.py`: HTML generation for the email content
- `dockerise.sh`: Shell script to build and push Docker image
- `Dockerfile`: Docker configuration for deployment
- `requirements.txt`: Python dependencies
- `.env`: Environment variables (not included in version control)