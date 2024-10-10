'''This script will check the database to see whether any subscribers require notification'''
import logging
from os import environ as ENV
from datetime import datetime as dt
from dotenv import load_dotenv
from psycopg2 import connect, extras

def get_connection():
    '''Returns a psycopg2 connection'''
    return connect(f"""dbname={ENV["DB_NAME"]} user={ENV["DB_USER"]}
                 host={ENV["DB_HOST"]} password={ENV["DB_PASSWORD"]} port={ENV["DB_PORT"]}""")

def get_subscribers() ->list[dict]:
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
    ba.at <= CURRENT_TIMESTAMP + INTERVAL '4 hours'
    AND ba.at > CURRENT_TIMESTAMP '''

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            subscribers = cur.fetchall()

    return [{'user':sub[0],'phone':sub[1],'email':sub[2],'body':sub[3],'time':sub[4]} for sub in subscribers]

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    get_subscribers()
