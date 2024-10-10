FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .
RUN pip install -r requirements.txt 

COPY api_error.py .
COPY pipeline.py .
COPY load.py .
COPY extract.py .
COPY transform.py .

CMD [ "pipeline.lambda_handler" ]