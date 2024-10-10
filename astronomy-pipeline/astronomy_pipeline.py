# astronomy_pipeline.py

import logging
from astronomy_extract import extract_weekly_astronomy_data
from astronomy_transform import transform_astronomy_data
from astronomy_load import get_db_connection, load_body_positions, load_moon_phases

from dotenv import load_dotenv
def lambda_handler():
    """
    AWS Lambda Handler Function that triggers the full pipeline:
    - Extract astronomical data.
    - Transform it into a format suitable for database loading.
    - Load the transformed data into the RDS database.
    """

    # Load environment variables from the .env file
    load_dotenv()

    logging.info("Lambda function triggered to run the astronomy ETL pipeline.")

    try:
        # Extract raw astronomy data
        raw_data = extract_weekly_astronomy_data()
        if not raw_data:
            return {
                'statusCode': 400,
                'body': 'No data found during extraction.'
            }

        # Transform the raw data
        transformed_data = transform_astronomy_data(raw_data)
        print('Transformed')

        # Establish a database connection
        conn = get_db_connection()

        # Load the transformed data into the database
        load_body_positions(conn, transformed_data['positions_list'])
        load_moon_phases(conn, transformed_data['moon_phase_list'])

        return {
            'statusCode': 200,
            'body': 'Astronomy data processed and loaded successfully.'
        }

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return {
            'statusCode': 500,
            'body': f"Failed to process and load the data: {e}"
        }
    

if __name__ == '__main__':
    lambda_handler()