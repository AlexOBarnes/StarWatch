'''Checks for todays NASA image of day and the current ISS coordinates'''
import sys
import os
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'weekly-openmeteo')))
from os import environ as ENV
import logging
from datetime import datetime as dt
from dotenv import load_dotenv
from requests import get
from psycopg2 import connect
from api_error import APIError
from extract import get_connection

KEYS = ['data','title','url']



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
        else:
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

def get_iss_location() -> dict:
    '''Requests the current ISS location'''
    ...

def transform_iss_data() -> list:
    '''Formats the ISS data ready for insertion'''
    ...

def load_iss_data() -> None:
    '''Uploads the data into the database'''
    ...


def iss_pipeline() -> None:
    '''Runs the ISS pipeline to obtain the current ISS location'''
    ...

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    nasa_pipeline()