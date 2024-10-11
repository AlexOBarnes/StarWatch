# Quadhoral OpenMeteo Pipeline
This folder contains the code for the [OpenMeteo API](https://open-meteo.com/en/docs) data pipeline. This includes `extract.py`, `transform.py`, `load.py` and `pipeline.py`. This pipeline uses the `requests` library to send HTML GET requests to the `OpenMeteo API` and the `psycopg2` library to load this data onto our database. The data requested includes `cloud cover`, `visibility` and `chance of precipitation`, this pipeline is therefore designed to run every four hours to ensure accurate data.

## Setup
1. Ensure that an SQL server RDS has been setup prior and is accessible
    - Note: be sure to store the credentials for accessing this database safely.

### To Run Locally:
2. Setup a venv and install the requirements
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Create a `.env` file with the following:
    - DB_HOST - to access your RDS instance
    - DB_USER - username for accessing RDS
    - DB_PASSWORD - password for accessing RDS
    - DB_NAME - the name of your database
    - DB_PORT - port to access RDS (typically 5432 for postgres)

### To Run on AWS:

2. Create an ECR repository through terraform or the AWS UI.
In order for your provisioned architecture one must dockerise their scripts and dependencies and push to an ECR repository.  
For the next steps you will require AWS credentials and the ECR URI.

3. Download the aws-cli:
```bash
brew install awscli
```
4. Verify your credentials:
```bash
aws configure
```
This will require sensitive information to be entered through the command line

5. Add to your `.env` file the following:
    - AWS_REGION - region of your ECR repository
    - ECR_URI - endpoint of the ECR repository
    - IMAGE_NAME - a name given to your docker image

6. Run the following command to automatically dockerise and push to ECR:
```bash
bash ../dashboard/deploy.sh
```
7. Now follow the terraform setup steps in the `../terraform` folder to provision a lambda based off this docker image.

## Usage
- To use locally one can use the following command:
```bash
python pipeline.py
```
It is a good idea to ensure that the pipeline works with your credentials prior to provisioning the AWS architecture

- To run tests run the following command:
```bash
pytest
```
Alternatively to run specific tests or test files:
```bash
pytest path/to/test_file.py
pytest path/to/test_file.py::test_function_name
```
To get a coverage report execute the following;
```bash
pytest --cov
```

## How it works
#### `quadhoral_extract.py`
- Sends a get request to the openmeteo API using the `requests` library.
- Obtains a list of coordinates for every county in the UK from the RDS using `psycopg2`.
#### `quadhoral_transform.py`
- Processes the weather data using base python and `datetime` library. 
- Returns data in a list of lists format suitable for batch upload.
#### `quadhoral_load.py`
- Uses `psycopg2` to firstly delete future forecasts then load the up to data weather data to the project database.
#### `quadhoral_lambda.py`
- Written to the AWS lambda style.
- Orchestrates the ETL pipeline. 
#### `quadhoral_test_[filename].py`
- Contains the tests for each file in this folder.
- Uses `pytest` and `unittest.mock` to test the ETL pipeline.
#### `conftest.py`
- Contains the `pytest.fixture` functions for the tests in this folder.