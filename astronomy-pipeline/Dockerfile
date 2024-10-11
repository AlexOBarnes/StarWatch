FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .
RUN pip install -r requirements.txt 

COPY astronomy_load.py .
COPY astronomy_extract.py .
COPY astronomy_transform.py .
COPY astronomy_extract_functions.py .
COPY astronomy_transform_functions.py .
COPY astronomy_lambda.py .

CMD [ "astronomy_lambda.lambda_handler" ]