'''Loads cleaned data into the RDS instance'''
import logging
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from quadhoral_extract import get_connection


def truncate_database() -> None:
    '''Removes future forecasts so that they can be replaced'''
    query = '''DELETE FROM forecast WHERE at >= CURRENT_TIMESTAMP'''
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()

def load_data(data: list[list]) -> None:
    '''Inserts data into a postgres database'''
    query = '''INSERT INTO forecast
    (county_id, at, temperature_c, precipitation_probability_percent, 
    precipitation_mm, cloud_coverage_percent, visibility_m) 
    VALUES %s'''
    with get_connection() as conn:
        with conn.cursor() as cur:
            execute_values(cur, query, data)
            conn.commit()

def load(data:list[list]) -> None:
    '''Runs load portion of ETL pipeline'''
    truncate_database()
    logging.info('Truncated database successfully')
    load_data(data)
    logging.info('%s rows inserted successfully',len(data))



if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    load([[]])
