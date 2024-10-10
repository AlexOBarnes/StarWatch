# Weekly OpenMeteo Pipeline
This folder contains the code for the [OpenMeteo API](https://open-meteo.com/en/docs) data pipeline. This includes `extract.py`, `transform.py`, `load.py` and `pipeline.py`. This pipeline uses the `requests` library to send HTML GET requests to the `OpenMeteo API` and the `psycopg2` library to load this data onto our database. The data requested includes `time of sunset` and `time of sunrise`. This pipeline is therefore designed to run every week as these are far more predictable values.

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
    - REGION - region of your ECR repository
    - ECR_URI - endpoint of the ECR repository
    - IMAGE_NAME - a name given to your docker image

6. Run the following command to automatically dockerise and push to ECR:
```bash
bash ../dashboard/deploy.sh
```
7. Now follow the terraform setup steps in the `../terraform` folder to provision a lambda based off this docker image

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
#### `extract.py`
- Uses `psycopg2` to query the county longitude and latitudes
- Sends a get request to the OpenMeteo API using the `requests` library
- Returns the a list of the data from the response of that API
#### `transform.py`
- Uses base `python` and `datetime` library to transform ata into a list of lists
#### `load.py`
- Uses `psycopg2` to bulk insert the solar feature data onto a given postgres database
#### `pipeline.py`
- Orchestrates the entire ETL pipeline
#### `api_error.py`
- Uses OOP to create a customisable error class for API errors
- Instantiates a new object with a status code and message
#### `test_[file_name]`
- Contains the tests for [file_name]
- Uses `pytest` and `unittest.mock` to idempotently test each module
#### `conftest.py`
- Uses `pytest.fixture` to create fixtures for the tests in this file