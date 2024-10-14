# SMS-Checker Pipeline
This folder contains the code for the SMS-checker application. This application can be triggered to query the database for any subscribers that are due an alert for a celestial body or aurora, this is done using the `psycopg2` library. These subscriber details are then used to send emails and SMS messages with the appropriate alerts using `boto3`.

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
    - AWS_ACCESS_KEY - your personal access key to AWS
    - AWS_SECRET_KEY - your personal secret key to AWS
    - AWS_REGION - the region of AWS that you will be using for this project

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
python notification_lambda.py
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
#### `checker.py`
- Uses `psycopg2` to query the RDS database and identify all users who will have a visible body within the next 3 hours.
- Returns a list of dictionaries with their phone, email and celestial body information.
#### `conftest.py`
- Contains the `pytest.fixture` for the tests in this folder.
#### `message.py`
- Uses `boto3` to create either a SES or SNS client to send emails or SMS' ,respectively.
- Uses `dotenv` to securely load these environment details
#### `notification_lambda.py`
- Written to follow the lambda function conventions
- Takes in event and context variables and orchestrates the SMS pipeline
#### `test_[filename]`
- Tests are consistently named with the file name they are testing
- Each test file has at least a 75% test coverage
- `pytest` and `unittest.mock` are used to test the files in this folder