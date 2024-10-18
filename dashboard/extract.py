'''Contains get_connection function'''
from os import environ as ENV
import logging
from dotenv import load_dotenv
from psycopg2 import connect
from requests import get
from api_error import APIError

URL = "https://api.open-meteo.com/v1/forecast"

def get_connection():
    '''Returns a psycopg2 connection'''
    return connect(f"""dbname={ENV["DB_NAME"]} user={ENV["DB_USER"]}
                 host={ENV["DB_HOST"]} password={ENV["DB_PASSWORD"]} port={ENV["DB_PORT"]}""")


def get_county_coordinates() -> tuple[list[int]]:
    '''Returns a params dict containing the UK counties coordinates'''
    query = '''SELECT longitude,latitude FROM county'''
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            counties = cur.fetchall()
    return [county[0] for county in counties], [county[1] for county in counties]


def convert_to_params(long: list[int], lat: list[int]):
    '''Converts the obtained longitude and latitude values to params'''
    if isinstance(lat, list) and isinstance(long, list):

        return {'latitude': lat, 'longitude': long,
                "daily": ["sunrise", "sunset"], "timezone": "Europe/London"}

    raise TypeError('Queried data is wrong datatype')


def request_solar_data(params: dict) -> list:
    '''Returns the solar data for the given set of coordinates'''
    response = get(URL, params=params, timeout=10)
    logging.info('Request sent.')

    if response.status_code == 200:
        logging.info('Get request successful.')
        solar_data = response.json()

        if isinstance(solar_data, list):

            if len(solar_data) == 106 and \
                    all(len(region['daily']['sunrise']) > 0 for region in solar_data) and \
                    all(len(region['daily']['sunset']) > 0 for region in solar_data):
                return solar_data

            raise ValueError('Missing Values in returned data')

        raise TypeError('Data returned is of wrong datatype')

    logging.info('Get request unsuccessful.')
    raise APIError('Unsuccessful request.', response.status_code)


def extract() -> list:
    '''Runs extract pipeline'''
    longitude, latitude = get_county_coordinates()
    parameters = convert_to_params(longitude, latitude)
    return request_solar_data(parameters)


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    logging.info('Environment loaded')
    extract()
