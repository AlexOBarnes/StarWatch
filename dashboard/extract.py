'''Contains get_connection function'''
from os import environ as ENV
from psycopg2 import connect
from dotenv import load_dotenv

def get_connection():
    '''Returns a psycopg2 connection'''
    return connect(f"""dbname={ENV["DB_NAME"]} user={ENV["DB_USER"]}
                 host={ENV["DB_HOST"]} password={ENV["DB_PASSWORD"]} port={ENV["DB_PORT"]}""")

