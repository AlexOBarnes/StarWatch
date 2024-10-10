# astronomy_load.py

import logging
from psycopg2 import connect, extensions
from psycopg2.extras import execute_values
from os import environ as ENV
from dotenv import load_dotenv

def get_db_connection() -> extensions.connection:
    """
    Establishes and returns a connection to the PostgreSQL database using environment variables.
    """
    load_dotenv()
    try:
        conn = connect(
            dbname=ENV["DB_NAME"],
            user=ENV["DB_USER"],
            host=ENV["DB_HOST"],
            password=ENV["DB_PASSWORD"],
            port=ENV.get("DB_PORT", "5432")  # Default port 5432 if not specified
        )
        logging.info("Database connection established.")
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to the database: {e}")
        raise


def load_body_positions(conn, positions_list):
    """Load body positions into the database."""
    query = """
    INSERT INTO body_assignment (region_id, body_id, at, distance_km, azimuth, altitude, constellation_id)
    VALUES %s
    """
    
    with conn.cursor() as cur:
        try:
            execute_values(cur, query, positions_list)
            conn.commit()
            logging.info("Body positions loaded successfully.")
        except Exception as e:
            logging.error(f"Error inserting into 'body_assignment': {e}")
            conn.rollback()

def load_moon_phases(conn, moon_phases: list) -> None:
    """
    Inserts moon phase records into the 'moon_phases' table.
    """
    query = """
        INSERT INTO moon_phases (
            phase_date,
            image_url
        ) VALUES %s
        ON CONFLICT DO NOTHING;
    """

    try:
        with conn.cursor() as cur:
            execute_values(cur, query, moon_phases)
            conn.commit()
            logging.info(f"Inserted {len(moon_phases)} records into 'moon_phases'.")
    except Exception as e:
        conn.rollback()
        logging.error(f"Error inserting into 'moon_phases': {e}")
        raise