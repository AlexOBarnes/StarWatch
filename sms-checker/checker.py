'''This script will check the database to see whether any subscribers require notification'''
import logging
from os import environ as ENV
from dotenv import load_dotenv
from psycopg2 import connect

def get_connection():
    '''Returns a psycopg2 connection'''
    return connect(f"""dbname={ENV["DB_NAME"]} user={ENV["DB_USER"]}
                 host={ENV["DB_HOST"]} password={ENV["DB_PASSWORD"]} port={ENV["DB_PORT"]}""")

def get_subscribers_bodies() ->list[dict]:
    '''Returns a list of dictionaries containing subscribers,
      bodies, time and notification service'''
    query = '''SELECT s.subscriber_username,s.subscriber_phone,
    s.subscriber_email,b.body_name,ba.at as body_time
    FROM subscriber_county_assignment as sca
    JOIN subscriber as s USING (subscriber_id)
    JOIN county as c USING (county_id)
    JOIN forecast as f USING (county_id)
    JOIN region as r USING (region_id)
    JOIN body_assignment as ba USING (region_id)
    JOIN body as b USING (body_id)
    WHERE f.visibility_m > 500 AND
    f.cloud_coverage_percent < 25 AND
    ba.at <= CURRENT_TIMESTAMP + INTERVAL '3 hours'
    AND ba.at > CURRENT_TIMESTAMP '''

    with get_connection() as conn:
        logging.info('Connection established')
        with conn.cursor() as cur:
            logging.info('Cursor generated')
            cur.execute(query)
            logging.info('Query executed')
            subscribers = cur.fetchall()

    return [{'user':sub[0],'phone':sub[1],'email':sub[2],
             'body':sub[3],'time':sub[4]} for sub in subscribers]

def get_aurora_regions():
    '''Returns a list of region ids for a given '''
    query = '''SELECT ac.colour,ac.meaning FROM aurora_alert
    JOIN aurora_colour as ac USING (aurora_colour_id)
    ORDER BY alert_time DESC
    LIMIT 1'''
    with get_connection() as conn:
        logging.info('Connection established.')
        with conn.cursor() as cur:
            cur.execute(query)
            data = cur.fetchall()[0]
            logging.info('Aurora alert query executed.')

    return data

def get_subscribers_aurora() -> list[dict]:
    '''Returns a list of dictionaries containing subscribers details 
    depending on aurora alert'''
    query = '''SELECT s.subscriber_username, s.subscriber_phone,
    s.subscriber_email FROM subscriber_county_assignment as sca
    JOIN subscriber as s USING (subscriber_id)
    JOIN county as c USING(county_id)
    JOIN forecast as f USING (county_id)
    JOIN region as r USING(region_id)
    WHERE f.cloud_coverage_percent < 50 AND
    f.visibility_m > 250'''

    colour = get_aurora_regions()
    logging.info('Current aurora alert level: %s',colour[0])
    if colour[0] == 'Green':
        return None,None
    if colour[0] == 'Yellow':
        query += 'AND r.region_id in [1,2,4,5,6]'

    with get_connection() as conn:
        logging.info('Connection established')
        with conn.cursor() as cur:
            cur.execute(query)
            data = cur.fetchall()
            logging.info('Query executed')

    return ([{'user': sub[0], 'phone': sub[1], 'email': sub[2]} for sub in data],colour)


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    get_subscribers()
