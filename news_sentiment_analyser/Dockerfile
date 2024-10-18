# Specifies latest image of python
FROM python:3.11

WORKDIR /app

# Copies txt file containing env package requirements
COPY requirements.txt .

# Pip installs required packages.
RUN pip install -r requirements.txt

# Copies working files.
COPY extract_s3.py .
COPY openai_topics.py .
COPY sentiment_analysis.py .
COPY transform_articles.py .
COPY load_rds.py .
COPY database_functions.py .
COPY pipeline_analysis.py .
COPY clean_content.py .

# Runs pipeline
CMD ["python3", "pipeline_analysis.py"]