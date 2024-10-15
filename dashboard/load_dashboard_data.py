import os

import psycopg2
from psycopg2.extensions import connection as Psycopg2Connection

import pandas as pd
from dotenv import load_dotenv


def return_connection():
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



if __name__ == '__main__':
    # Main block, primarily for testing.
    load_dotenv()

    conn_instance = return_connection()
    print(load_from_starwatch_rds(conn_instance, 'forecast'))