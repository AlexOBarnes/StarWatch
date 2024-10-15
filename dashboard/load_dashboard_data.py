import os

import psycopg2
from psycopg2.extensions import connection as Psycopg2Connection

import pandas as pd
from dotenv import load_dotenv
import streamlit as st


def connect_to_db():
    '''Returns a psycopg2 connection object'''

    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
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
            query = f"""
            SELECT *
            FROM {table_name};
            """

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
            query = f"""
            SELECT *
            FROM forecast AS f
            JOIN county AS c
            ON f.county_id = c.county_id;
            """

            cur.execute(query)
            data = cur.fetchall()

            columns = [desc[0] for desc in cur.description]

    df = pd.DataFrame(data, columns=columns)

    return df






if __name__ == '__main__':
    # Main block, primarily for testing.
    load_dotenv()

    conn_instance = connect_to_db()
    print(load_from_starwatch_rds(conn_instance, 'forecast'))
