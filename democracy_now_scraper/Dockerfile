# Specifies latest image of python
FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

# Copies txt file containing env package requirements
COPY requirements.txt .

# Pip installs required packages.
RUN pip install -r requirements.txt

# Copies working files.
COPY load_dn.py .
COPY transform_dn.py .
COPY extract_dn.py .
COPY pipeline_dn.py .


# Runs pipeline
CMD ["pipeline_dn.lambda_handler"]