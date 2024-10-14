'''Checks for todays NASA image of day and the current ISS coordinates'''
import sys
import os
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'weekly-openmeteo')))
from os import environ as ENV
from dotenv import load_dotenv
from requests import get
from psycopg2 import connect
from api_error import APIError


def has_nasa_image() -> bool:
    '''Returns a boolean for whether the stored nasa image is up to data'''
    ...

def get_nasa_image():
    '''Requests todays nasa image'''
    ...

def load_image():
    '''Loads the nasa image onto the database'''
    ...

def get_iss_location() -> dict:
    '''Requests the current ISS location'''
    ...

def transform_iss_data() -> list:
    '''Formats the ISS data ready for insertion'''
    ...

def load_iss_data() -> None:
    '''Uploads the data into the database'''
    ...

def nasa_pipeline() -> None:
    '''Runs the nasa pipeline to upload the nasa image for the day.'''
    ...

def iss_pipeline() -> None:
    '''Runs the ISS pipeline to obtain the current ISS location'''
    ...