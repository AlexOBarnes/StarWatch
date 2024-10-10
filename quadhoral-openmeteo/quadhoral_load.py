'''Loads cleaned data into the RDS instance'''
import logging
from dotenv import load_dotenv
from quadhoral_extract import get_connection


def load_data(data: list[list]) -> None:
    '''Inserts data into a postgres database'''
    ...


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    load_data([[]])
