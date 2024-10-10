'''Orchestrates weekly ETL pipeline'''
# pylint: disable=W0612,W0613,E0606
import logging

from aurora_extract import extract
from aurora_transform import transform
from aurora_load import load_data


def lambda_handler(event, context):
    '''Orchestrates ETL pipeline for the AuroraWatch UK API data.'''
    logging.basicConfig(level=logging.INFO)
    data = extract()

    if data:
        clean_data = transform(data)

    if clean_data:
        load_data(clean_data)


if __name__ == '__main__':
    lambda_handler({}, {})
