# 📊 News Sentiment Analyser

## 📋 Overview 
The news sentiment analyser pipeline links topics to articles by querying a ChatGPT model and runs sentiment analysis article headings and content using VADER polarity scores.  
The pipeline is designed to retrieve dataframes stored in an S3 bucket and then write the results to a PostgreSQl database.

## 🛠️ Prerequisites
- **Docker** installed.
- Setup **ECR** repository to store analyser pipeline docker image.  

Optional:
- **Python** installed (For running locally)

## ⚙️ Setup 
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
    OPENAI_MODEL=<your-openai-model>
    ```

### ☁️ Pushing to the Cloud
To deploy the overall cloud infrastructure the sentiment analyser pipeline must be containerised and hosted on the cloud:

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
The sentiment analysis pipeline can also be ran locally by:

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
    python3 pipeline_analysis.py
    ```

```
Name                         Stmts   Miss  Cover
------------------------------------------------
clean_content.py                17      1    94%
database_functions.py           39      7    82%
extract_s3.py                   37      1    97%
load_rds.py                     40      3    92%
openai_topics.py                55      6    89%
sentiment_analysis.py           18      1    94%
------------------------------------------------
TOTAL                          548     19    97%
```

## Methodology 

Sentiment analysis is performed using (VADER)[https://ojs.aaai.org/index.php/ICWSM/article/view/14550]. VADER is a rule-based sentiment analyser which can map the "intensity" and nature of emotions to a score. Passed to the database is a compound score for the `title` and `content`, normalised to lie in the range $[-1,1]$. As for topic labelling, we begin with a pre-set list. Articles are mapped to 0, 1 or more topics, depending on their title. This is handled using `gpt-4o-mini` OpenAI model.

- [ ] Possibly more detail here on topics

### ✅ Test coverage
To generate a detailed test report:
```bash
pytest -vv
```
To include coverage results:
```bash
pytest --cov -vv
```
