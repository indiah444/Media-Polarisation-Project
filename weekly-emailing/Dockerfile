# Specifies latest image of python
FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

# Copies txt file containing env package requirements
COPY requirements.txt .

# Pip installs required packages.
RUN pip install -r requirements.txt

# Copies working files.
COPY w_db_funcs.py .
COPY pdf_content.py .
COPY graphs.py .
COPY weekly_email.py .


# Runs pipeline
CMD ["weekly_email.lambda_handler"]