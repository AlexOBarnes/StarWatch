'''Extracts weather data for each county for the next day'''
import logging
from os import environ as ENV
import psycopg2
from dotenv import load_dotenv

def get_connection():
    '''Returns a psycopg2 connection'''
    ...

def get_county_coordinates() -> tuple(str):
    '''Returns a tuple of county coordinate strings'''
    ...

def request_weather_data() -> list[dict]:
    '''Sends a get request for the weather data'''
    ...

if __name__ == '__main__':
    ...