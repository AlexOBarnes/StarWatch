'''Script to load the transformed data from the AuroraWatch UK API into the database.'''

from os import environ as ENV
import logging

from psycopg2 import connect, extensions
from dotenv import load_dotenv

from aurora_extract import extract
from aurora_transform import transform


def get_connection() -> extensions.connection:
    '''Returns a psycopg2 connection given the loaded environment variables.'''
    load_dotenv()

    return connect(f'''dbname={ENV["DB_NAME"]} user={ENV["DB_USER"]}
                 host={ENV["DB_HOST"]} password={ENV["DB_PASSWORD"]} port={ENV["DB_PORT"]}''')


def load_data(alert_data: tuple) -> None:
    '''Loads the given AuroraWatch Tuple into the connected database.'''
    query = '''INSERT INTO aurora_alert (alert_time, aurora_colour_id) VALUES (%s,%s);'''

    with get_connection() as conn:
        logging.info('Connected to database.')
        with conn.cursor() as cur:
            cur.execute(query, alert_data)
            conn.commit()
            logging.info('New aurora alert data inserted.')


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    extracted_data = extract()
    transformed_data = transform(extracted_data)
    load_data(transformed_data)
