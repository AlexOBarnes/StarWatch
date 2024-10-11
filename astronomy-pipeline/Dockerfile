<<<<<<< HEAD
=======

>>>>>>> a0df15d8d63cdd7a0da2ce784e2aa801c99da459
FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .
<<<<<<< HEAD
RUN pip install -r requirements.txt 

COPY astronomy_load.py .
COPY astronomy_extract.py .
COPY astronomy_transform.py .
COPY astronomy_extract_functions.py .
COPY astronomy_transform_functions.py .
COPY astronomy_lambda.py .

CMD [ "astronomy_lambda.lambda_handler" ]
=======
RUN pip install -r requirements.txt

COPY astronomy_load.py .
COPY astronomy_extract.py .
COPY astronomy_extract_functions.py .
COPY astronomy_transform.py .
COPY astronomy_transform_functions.py .
COPY astronomy_pipeline.py .



# Set the CMD to point to the Lambda handler
CMD ["astronomy_pipeline.lambda_handler"]
>>>>>>> a0df15d8d63cdd7a0da2ce784e2aa801c99da459
