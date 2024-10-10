'''This script will check the database to see whether any subscribers require notification'''
import logging
from dotenv import load_dotenv
from psycopg2 import connect, extras

def get_connection():
    '''Returns a psycopg2 connection'''
    ...

def get_subscribers() ->list[dict]:
    '''Returns a list of dictionaries containing subscribers,
      bodies, time and notification service'''
    ...

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
