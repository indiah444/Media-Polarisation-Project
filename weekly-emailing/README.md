
# 🗓️ ✉️ Weekly Media Sentiment Email Report

## 📋 Overview
This project automates the process of sending a weekly email report that includes an analysis of media sentiment from various sources. The report compiles data from the previous week, calculates the average sentiment polarity by topic and source, and generates a PDF that is attached to the email sent to subscribers.

The project consists of scripts to:
- Interact with a PostgreSQL database.
- Generate a PDF report based on sentiment analysis, including graphs for average polarity scores and sentiment distribution across various topics and sources.
- Send emails using AWS SES.
- Deploy the functionality using Docker and AWS Lambda.

## 🛠️ Prerequisites
- **Docker** installed.
- Setup **ECR** repository to store weekly email generator docker image.  

Optional:
- **Python** installed (For running locally)

## ⚙️ Setup 
Create a `.env` file with the following environment variables:
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

# ECR Configuration
ECR_REGISTRY_ID=<id_of_ecr_repo_to_store_image>
ECR_REPO_NAME=<name_of_ecr_repo_to_store_image>
IMAGE_NAME=weekly-email-image  # or any other appropriate name

# Emailing Configuration
FROM_EMAIL=<your_ses_verified_email>
```

### ☁️ Pushing to the Cloud
To deploy the overall cloud infrastructure, the weekly email generator must be containerised and hosted on the cloud:

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
The weekly email generator can also be ran locally by:

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
    python3 weekly_email.py
    ```

## 📁 Files
- `weekly_email.py`: Script to send a weekly email report
- `w_db_funcs.py`: Database interaction functions
- `pdf_content.py`: PDF generation for the email attachment
- `graphs.py`: Functions tat create graphs for the PDF
- `dockerise.sh`: Shell script to build and push Docker image
- `Dockerfile`: Docker configuration for deployment
- `requirements.txt`: Python dependencies
- `.env`: Environment variables (not included in version control)

### ✅ Test coverage
To generate a detailed test report:
```bash
pytest -vv
```
To include coverage results:
```bash
pytest --cov -vv
```