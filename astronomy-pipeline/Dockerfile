
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Copy the .env file to the container
COPY .env .env

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the CMD to point to the Lambda handler
CMD ["python", "astronomy_pipeline.py"]