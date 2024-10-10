'''Transforms data obtained from openmeteo ready for loading'''
import logging
from datetime import datetime as dt


def format_time(event_time: str) -> dt:
    '''Returns a datetime object from a string'''
    return dt.strptime(event_time, '%Y-%m-%dT%H:%M')

def clean_data(county_data: dict) -> dict:
    '''Returns a dictionary of weather data'''
    return {'time': county_data['hourly']['time'],
            'temp': county_data['hourly']['temperature_2m'],
            'prob': county_data['hourly']['precipitation_probability'],
            'precip': county_data['hourly']['precipitation'],
            'clouds': county_data['hourly']['cloud_cover'],
            'visibility': county_data['hourly']['visibility']}

def format_data(clean_county_data: dict, county_id: int) -> list[list]:
    '''Returns a list of lists containing county_id and weather data'''
    if not clean_county_data['time']:
        return []

    return [[county_id, format_time(clean_county_data['time'][i]),
             clean_county_data['temp'][i], clean_county_data['prob'][i],
             clean_county_data['precip'][i], clean_county_data['clouds'][i],
             clean_county_data['visibility'][i]]
             for i in range(len(clean_county_data['time']))]

def transform(data: list[dict]) -> list[list]:
    '''Orchestrates transform steps of pipeline'''
    if not data:
        raise ValueError('No data to transform.')

    formatted_data = []
    logging.info('Data transformation begun.')

    for county_id, county in enumerate(data, 1):
        logging.info('Cleaning data for county: %s.', county_id)
        clean_county = clean_data(county)
        formatted_data.extend(format_data(clean_county, county_id))
        logging.info('Data cleaning for county %s complete.', county_id)

    logging.info('Data tranformation complete.')
    logging.info('Number of rows to insert: %s', len(formatted_data))
    return formatted_data


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    transform([{}])
