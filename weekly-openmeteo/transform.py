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
    if not data:
        raise ValueError('No data to transform.')

    formatted_data = []
    logging.info('Data transformation begun.')

    for county_id,county in enumerate(data,1):
        logging.info('Cleaning data for county: %s.',county_id)
        clean_county = clean_data(county)
        formatted_data.extend(format_data(clean_county,county_id))
        logging.info('Data cleaning for county %s complete.', county_id)

    logging.info('Data tranformation complete.')
    logging.info('Number of rows to insert: %s',len(formatted_data))
    return formatted_data


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    transform([{}])
