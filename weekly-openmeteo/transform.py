'''Transforms solar data and ready for loading'''
import logging
from dotenv import load_dotenv
from extract import get_connection

def get_county_ids() -> dict:
    '''Returns a dictionary of longitude to county_id'''
    ...

def clean_data(county_data: dict) -> dict:
    '''Returns a dictionary of county_id, sunset and sunrise times'''
    ...

def format_data(clean_county_data: dict) -> list[list]:
    '''Returns a list of lists containing county_id, sunset and sunrise times'''
    ...


def transform(data: list[dict]) -> list[list]:
    '''Returns a list of lists containing county_id, sunset and sunrise times'''
    ...

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    logging.info('Environment variables loaded.')
    transform()