FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .
RUN pip install -r requirements.txt 

COPY api_error.py .
COPY quadhoral_lambda.py .
COPY quadhoral_load.py .
COPY quadhoral_extract.py .
COPY quadhoral_transform.py .

CMD [ "quadhoral_lambda.lambda_handler" ]