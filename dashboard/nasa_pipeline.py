'''Checks for todays NASA image of day and the current ISS coordinates'''
#pylint: disable=E0401,C0413
from os import environ as ENV
import sys
import os
import logging
from datetime import datetime as dt
from dotenv import load_dotenv
from requests import get

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'weekly-openmeteo')))
from api_error import APIError
from extract import get_connection

KEYS = ['data','title','url']

def get_image_of_the_day() -> str:
    query = """SELECT image_name,image_url FROM image
    WHERE image_name ILIKE '%nasa_%' AND
     image_date = CURRENT_DATE """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            data = cur.fetchone()
    return data

def get_moon_phase() -> str:
    '''Returns todays moon phase'''
    query = """SELECT image_url FROM image
    WHERE image_name = 'moon_phase' AND
    image_date = CURRENT_DATE"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            data = cur.fetchone()
    return data[0]


def has_nasa_image() -> bool:
    '''Returns a boolean for whether the stored nasa image is up to data'''
    query = """SELECT COUNT(*) FROM image
    WHERE image_name ILIKE '%nasa_%' AND
     image_date = CURRENT_DATE """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            data = cur.fetchone()
    return bool(data[0])


def extract_time(time_str: str) -> dt:
    '''Returns a datetime object'''
    return dt.strptime(time_str,'%Y-%m-%d')

def get_nasa_image():
    '''Requests todays nasa image'''
    url = f'https://api.nasa.gov/planetary/apod?api_key={ENV['NASA_API_KEY']}'
    response = get(url, timeout=10)


    if response.status_code == 200:
        data = response.json()
        clean_data = [extract_time(data.get('date')),f'NASA_{data.get('title')}',data.get('url')]
        if all(clean_data):
            logging.info('Data cleaned successfully.')
            return clean_data

        raise ValueError(f'Could not obtain {KEYS[clean_data.index(None)]}')

    raise APIError('Unsuccessful request.', response.status_code)


def load_image(data: list) -> None:
    '''Loads the nasa image onto the database'''
    query = '''INSERT INTO image (image_date,image_name,image_url)
    VALUES (%s,%s,%s)'''
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query,data)
            conn.commit()

def nasa_pipeline() -> None:
    '''Runs the nasa pipeline to upload the nasa image for the day.'''
    if not has_nasa_image():
        logging.info('No nasa image found for today.')
        image = get_nasa_image()
        logging.info('Nasa image identified')
        load_image(image)
        logging.info('Nasa image uploaded')
    logging.info('Nasa image found in database.')

def extract_unix_time(timestamp:int) -> dt:
    '''Converts a unix timestamp to a datetime object'''
    return dt.fromtimestamp(timestamp)

def get_iss_location() -> dict:
    '''Requests the current ISS location'''
    url = 'http://api.open-notify.org/iss-now.json'
    response = get(url, timeout=10)

    if response.status_code == 200:
        data = response.json()

        if data['message'] == 'success':
            return {'timestamp':extract_unix_time(data['timestamp']),
                    'latitude': data['iss_position']['latitude'],
                    'longitude':data['iss_position']['longitude']}

    raise APIError('Unsuccessful request.', response.status_code)

def get_sunset_times(region: str) -> tuple:
    '''Returns the sunset and sunrise time for a given region'''
    query = '''SELECT sunrise_timestamp, sunset_timestamp
    FROM solar_feature
    JOIN county USING (county_id)
    WHERE county_name ILIKE %s
    AND (DATE(sunrise_timestamp) = CURRENT_DATE
    OR DATE(sunrise_timestamp) = CURRENT_DATE + INTERVAL '1 day')
    ORDER BY sunrise_timestamp DESC
    LIMIT 2'''

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query,(region,))
            data = cur.fetchall()

    return (data[0][1],data[1][0])
    
if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    print(get_moon_phase())
