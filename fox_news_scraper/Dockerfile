FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY clean_fn.py .
COPY extract_fn.py .
COPY load_csv_fn.py .
COPY pipeline_fn.py .

CMD [ "pipeline_fn.lambda_handler" ]