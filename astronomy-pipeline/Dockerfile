FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY astronomy_load.py .
COPY astronomy_extract.py .
COPY astronomy_transform.py .
COPY astronomy_pipeline.py .

# Set the CMD to point to the Lambda handler
CMD ["astronomy_pipeline.lambda_handler"]

