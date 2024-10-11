# Astronomy API Pipeline
This folder contains the code for the `Astronomy API` data pipeline. This includes `extract.py`, `transform.py`, `load.py` and `pipeline.py`. This pipeline uses the `requests` library to send HTML GET requests to the [Astronomy API](https://docs.astronomyapi.com/) and the `psycopg2` library to load this data onto our database.

## Setup
1. Ensure that an SQL server RDS has been setup prior and is accessible
    - Note: be sure to store the credentials for accessing this database safely.

2. Signup for the [Astronomy API](https://astronomyapi.com/auth/signup) and store the id and secret key you receive securely

### To Run Locally:
3. Setup a venv and install the requirements
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
4. Create a `.env` file with the following:
    - DB_HOST - to access your RDS instance
    - DB_USER - username for accessing RDS
    - DB_PASSWORD - password for accessing RDS
    - DB_NAME - the name of your database
    - DB_PORT - port to access RDS (typically 5432 for postgres)
    - ASTRONOMY_ID - obtained when signing up for the astronomy API
    - ASTRONOMY_SECRET - secret key used for accessing the astronomy API

### To Run on AWS:

3. Create an ECR repository through terraform or the AWS UI.
In order for your provisioned architecture one must dockerise their scripts and dependencies and push to an ECR repository.  
For the next steps you will require AWS credentials and the ECR URI.

4. Download the aws-cli:
```bash
brew install awscli
```
5. Verify your credentials:
```bash
aws configure
```
This will require sensitive information to be entered through the command line

6. Add to your `.env` file the following:
    - AWS_REGION - region of your ECR repository
    - ECR_URI - endpoint of the ECR repository
    - IMAGE_NAME - a name given to your docker image

7. Run the following command to automatically dockerise and push to ECR:
```bash
bash deploy.sh
```
8. Now follow the terraform setup steps in the `../terraform` folder to provision a lambda based off this docker image.

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
#### `astronomy_extract.py`
- Orchestrates the extract portion of the pipeline
- Uses `json `and `datetime` to partially process the data before transform steps
#### `astronomy_extract_functions.py`
- Encodes the `auth_string` which is necessary for accessing the API
- Uses `psycopg2` to obtain the UK region coordinates
- Uses `requests` to send a get request for celestial body data from the Astronomy API, as well as, moon phase data.
#### `astronomy_transform.py`
- Orchestrates the transform portion of the pipeline
#### `astronomy_transform_functions.py`
- Utilises `pandas`, `datetime` and `json` to create a dataframe and process the obtained data
#### `astronomy_load.py`
- Uploads the list generated from the `pandas` dataframe to the project database using `psycopg2`
#### `astronomy_pipeline.py`
- Written to conform to AWS lambda conventions
- Orchestrates entire ETL pipeline
#### `test_astronomy_[filename].py`
- Contains the tests for the files within this folder
- Uses `pytest` and `unittest.mock` for each test
#### `deploy.sh`
- Runs a series of commands that dockerise the pipeline using the local `Dockerfile`.
- Pushes the docker image to a given ECR repository
#### `db_connect.sh`
- Connects to the project database using `.env` variables