'''This script loads the formatted sunrise and sunset times onto the postgres database'''
import logging
from dotenv import load_dotenv
from extract import get_connection

def load_data(data: list[list]) -> None:
    '''Inserts data into a postgres database'''
    ...

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    load_data([[]])
