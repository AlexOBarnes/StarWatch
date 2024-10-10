'''Transforms data obtained from openmeteo ready for loading'''
import logging
from datetime import datetime as dt


def format_time(event_time: str) -> dt:
    '''Returns a datetime object from a string'''
    ...

def clean_data(county_data: dict) -> dict:
    '''Returns a dictionary of weather data'''
    ...

def format_data(clean_county_data: dict, county_id: int) -> list[list]:
    '''Returns a list of lists containing county_id and weather data'''
    ...

def transform():
    '''Orchestrates transform steps of pipeline'''
    ...


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    transform([{}])
