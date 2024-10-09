'''Extracts weekly sunset and sunrise data for the 12 UK regions'''
import logging
from requests import get
from api_error import APIError

URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {"latitude": [54.61, 56.49, 52.13, 54.97, 53.78, 53.8,
                       52.9, 52.48, 52.24, 51.51, 51.28, 50.78],
	      "longitude": [-6.62, -4.2, -3.78, -1.61, -2.7, -1.54,
                       -1.23, -1.89, 0.9, -0.13, -0.78, -3.79],
	      "daily": ["sunrise", "sunset"],"timezone": "Europe/London"}

def extract() -> dict:
    '''Returns the solar data for the given set of coordinates'''
    response = get(URL, params=PARAMS, timeout=10)
    logging.info('Request sent.')

    if response.status_code == 200:
        logging.info('Get request successful.')
        solar_data = response.json()

        if isinstance(solar_data,list):

            if len(solar_data) == 12 and \
                all(len(region['daily']['sunrise']) > 0 for region in solar_data) and \
                all(len(region['daily']['sunset']) > 0 for region in solar_data):
                return solar_data

            raise ValueError('Missing Values in returned data')

        raise TypeError('Data returned is of wrong datatype')

    logging.info('Get request unsuccessful.')
    raise APIError('Unsuccessful request.',response.status_code)



if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    extract()
