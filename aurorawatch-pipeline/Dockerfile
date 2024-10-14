FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .
RUN pip install -r requirements.txt 

COPY aurora_load.py .
COPY aurora_extract.py .
COPY aurora_transform.py .
COPY aurora_pipeline.py .

CMD [ "aurora_pipeline.lambda_handler" ]