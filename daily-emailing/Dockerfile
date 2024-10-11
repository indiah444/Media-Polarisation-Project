# Specifies latest image of python
FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

# Copies txt file containing env package requirements
COPY requirements.txt .

# Pip installs required packages.
RUN pip install -r requirements.txt

# Copies working files.
COPY d_db_funcs.py .
COPY html_content.py .
COPY daily_email.py .


# Runs pipeline
CMD ["daily_email.lambda_handler"]