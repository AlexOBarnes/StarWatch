import os

import psycopg2
from psycopg2.extensions import connection as Psycopg2Connection

import pandas as pd
from dotenv import load_dotenv
import streamlit as st
import numpy as np
from tqdm import tqdm


def connect_to_db():
    '''Returns a psycopg2 connection object'''

    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        port = os.getenv('PORT'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )


def load_from_starwatch_rds(conn:Psycopg2Connection, table_name:str) -> pd.DataFrame:
    ''' 
    Retrieve all records from a passed in table name and returns that data
    as a pandas DataFrame, for a given psycogpg2 database connection.
    '''

    with conn:
        with conn.cursor() as cur:
            query = f'''
            SELECT *
            FROM {table_name};
            '''

            cur.execute(query)
            data = cur.fetchall()

            columns = [desc[0] for desc in cur.description]

    df = pd.DataFrame(data, columns=columns)

    return df



def load_forecasts_by_county_name(conn:Psycopg2Connection) -> pd.DataFrame:
    '''
    Returns a DataFrame of forecasted weather data joined with county
    information from the the StarWatch RDS.
    '''

    with conn:
        with conn.cursor() as cur:
            query = f'''
            SELECT *
            FROM forecast AS f
            JOIN county AS c
            ON f.county_id = c.county_id;
            '''

            cur.execute(query)
            data = cur.fetchall()

            columns = [desc[0] for desc in cur.description]

    df = pd.DataFrame(data, columns=columns)

    return df


def load_celestial_body_information(conn: psycopg2.extensions.connection, chunk_size: int = 1000) -> pd.DataFrame:
    '''
    Returns a DataFrame of forecasted weather data joined with county
    information from the StarWatch RDS, with progress tracking during fetching.
    '''
    
    query = '''
    with af as(SELECT r.region_id, r.region_name,f.at, AVG(f.cloud_coverage_percent)
    AS avg_cloud, AVG(f.visibility_m) AS avg_vis 
    FROM region AS r 
    JOIN county AS c
    USING(region_id) 
    JOIN forecast as f 
    USING (county_id) 
    WHERE EXTRACT(HOUR FROM f.at) >= 17 
    OR EXTRACT(HOUR FROM f.at) <= 5 
    GROUP BY r.region_id, r.region_name, f.at), br as
    (SELECT b.body_name,r.region_id, region_name,ba.at 
    FROM body AS b 
    JOIN  body_assignment AS ba
    USING (body_id) JOIN region AS r 
    USING (region_id) WHERE b.body_name NOT ILIKE 'Sun') 
    SELECT af.region_id, br.region_name,br.body_name,br.at,af.avg_cloud, af.avg_vis 
    FROM af JOIN br ON af.region_id = br.region_id AND br.at 
    = af.at;
        '''
    
    try:
        with conn:
            with conn.cursor() as cur:
                print('Starting query execution...')

                cur.execute(f'SELECT COUNT(*) FROM ({query}) AS total_query')
                total_rows = cur.fetchone()[0]
                print(f'Total rows to fetch: {total_rows}')

                cur.execute(query)
                
                df = pd.DataFrame()
                pbar = tqdm(total=total_rows, desc='Fetching data')

                while True:
                    print('Fetching a chunk...')
                    chunk = cur.fetchmany(chunk_size)
                    if not chunk:
                        break

                    chunk_df = pd.DataFrame(chunk, columns=[desc[0] for desc in cur.description])
                    df = pd.concat([df, chunk_df], ignore_index=True)
                    pbar.update(len(chunk))
                
                pbar.close()
        
        print('Data fetching complete.')
        return df
    
    except Exception as e:
        print(f'Error occurred: {e}')
        return pd.DataFrame()  


if __name__ == '__main__':

    load_dotenv()

    def starwatch_coefficient(visibility_m: float, distance_km: float, cloud_coverage_percent: float, k: float) -> float:
        '''
        Calculates the starwatch coefficient based on visibility, distance, 
        and cloud coverage using a weighted formula and sigmoid normalization.
        '''
        visibility_fraction = visibility_m / distance_km
        visibility_weighted = visibility_fraction ** 0.10
        adjusted_cloud_coverage = 1 - (cloud_coverage_percent / 100) ** 3
        coefficient = visibility_weighted * adjusted_cloud_coverage
        sigmoid_coefficient = 1 / (1 + np.exp(-10 * (coefficient - 0.5)))
        return max(0, min(sigmoid_coefficient, 1))

    conn = connect_to_db()
    print('Loading celestial body information...')
    bodies_df = load_celestial_body_information(conn)

    if not bodies_df.empty:
        tqdm.pandas()  
        bodies_df['visibility_coefficient'] = bodies_df.progress_apply(
            lambda row: starwatch_coefficient(row['visibility_m'], row['distance_km'], row['cloud_coverage_percent'], k=0.01),
            axis=1
        )

        print(bodies_df.tail(10))
        bodies_df.to_csv('test.csv')
    else:
        print('No data fetched. Exiting.')