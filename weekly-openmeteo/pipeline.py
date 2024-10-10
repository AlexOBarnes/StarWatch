'''Orchestrates weekly ETL pipeline'''
#pylint: disable=W0612,W0613,E0606
import logging
from dotenv import load_dotenv
from extract import extract
from transform import transform
from load import load_data

def lambda_handler(event, context):
    '''Orchestrates ETL pipeline for weekly OpenMeteo data'''
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    load_dotenv()
    logging.info('Environment loaded.')

    data = extract()

    if data:
        logging.info('Data extracted.')
        clean_data = transform(data)

    if clean_data:
        logging.info('Data cleaned.')
        load_data(clean_data)
        logging.info('Data loaded.')

if __name__ == '__main__':
    lambda_handler({},{})
