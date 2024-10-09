# Specifies latest image of python
FROM python:latest

WORKDIR /app

# Copies txt file containing env package requirements
COPY requirements.txt .

# Pip installs required packages.
RUN pip install -r requirements.txt

# Copies working files.
COPY extract_s3.py .

# Runs pipeline
CMD ["python3", "extract_s3.py"]