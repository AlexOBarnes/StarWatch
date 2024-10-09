'''Transforms solar data and ready for loading'''
import logging
from datetime import datetime as dt

def format_time(event_time: str) -> dt:
    '''Returns a datetime object from a string'''
    return dt.strptime(event_time,'%Y-%m-%dT%H:%M')

def clean_data(county_data: dict) -> dict:
    '''Returns a dictionary of county_id, sunset and sunrise times'''
    return {'sunrise':county_data['daily']['sunrise'],
            'sunset':county_data['daily']['sunset']}

def format_data(clean_county_data: dict, county_id: int) -> list[list]:
    '''Returns a list of lists containing county_id, sunset and sunrise times'''
    return [[county_id, format_time(clean_county_data['sunrise'][i]),
            format_time(clean_county_data['sunset'][i])] for i in range(7)]

def transform(data: list[dict]) -> list[list]:
    '''Returns a list of lists containing county_id, sunset and sunrise times'''
    ...


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    transform([{}])
