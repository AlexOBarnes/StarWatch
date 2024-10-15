"""Load functions to upload nested list data to relevant tables."""

import logging

from psycopg2.extras import execute_values

from astronomy_extract import get_db_connection


def upload_body_position_data(body_data: list[list]) -> None:
    '''Uploads the body position data to the database.'''
    # Positions list order [timestamp, distance_km, azimuth,
    #                       altitude, region_id, body_id,
    #                       constellation_id]

    with get_db_connection() as conn:
        logging.info("Connection established.")

        cur = conn.cursor()

        q_str = """
                INSERT INTO body_assignment
                (at, distance_km, azimuth, altitude, region_id, body_id, constellation_id)
                VALUES
                %s"""

        execute_values(cur, q_str, body_data)
        logging.info("Body position data uploaded.")


def upload_moon_phase_data(moon_phase_data: list[list]) -> None:
    '''Uploads the moon phase image data to the database.'''
    for entry in moon_phase_data:
        for _ in range(2):
            entry.append(None)
        entry.append("moon_phase")

    # Moon phase list order: [date, url, none, none, image_name]

    with get_db_connection() as conn:
        logging.info("Connection established.")

        cur = conn.cursor()

        q_str = """
                INSERT INTO image
                (image_date, image_url, region_id, constellation_id, image_name)
                VALUES
                %s"""

        execute_values(cur, q_str, moon_phase_data)
        logging.info("Moon phase data uploaded.")


def upload_star_chart_data(star_chart_data: list[list]) -> None:
    '''Uploads the star chart image data to the database.'''

    pass


def upload_astronomy_data(data_dict: dict) -> None:
    '''Uploads both the position and  moon phase data from the given dict.'''

    logging.info("Data upload to RDS started.")

    position_data = data_dict["positions_list"]
    moon_data = data_dict["moon_phase_list"]
    star_chart_data = data_dict["star_chart_list"]

    upload_body_position_data(position_data)
    upload_moon_phase_data(moon_data)
    upload_star_chart_data(star_chart_data)
