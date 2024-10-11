# Use official Python image as base
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the default port that Streamlit uses
EXPOSE 8501

# Command to run your app
CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]