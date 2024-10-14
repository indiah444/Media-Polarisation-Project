# 📊 News Sentiment Analyser
The news sentiment analyser pipeline links topics to articles by querying a ChatGPT model and runs sentiment analysis article headings and content using VADER polarity scores.  
The pipeline is designed to retrieve dataframes stored in an S3 bucket and then write the results to a PostgreSQl database.

## 🛠️ Prerequisites
- **Docker** installed.
- Setup **ECR** repository to store analyser pipeline docker image.  

Optional:
- **Python** installed (For running locally)

## 📂 Setup 
1. Create a `.env` file and fill with the following variables
    ```env
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
    IMAGE_NAME=article-analyser-image  # or any other appropriate name

    # OpenAI Configuration
    OPENAI_API_KEY=<your_openai_key>
    ```

### ☁️ Pushing to the Cloud
1. Make sure you have the Docker application running in the background
2. Dockerise and upload the application:
    ```bash
    bash dockerise.sh
    ```
    This will:
    - Authenticate your aws credentials with docker
    - Create the docker image
    - Tag the docker image
    - Upload tagged imgae to the ECR repository

### 💻 Running Locally (MacOS)
The sentiment analysis pipeline can also be ran locally by:

1. Creating and activating virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
2. Running the pipeline:
    ```bash
    python3 pipeline_analysis.py
    ```

## Test coverage

## Methodology 


### OpenAI API


### Sentiment Analysis 


#### Further improvements 