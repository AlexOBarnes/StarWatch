"""Load functions to upload nested list data to relevant tables."""

from psycopg2.extras import execute_values

from astronomy_extract_functions import get_db_connection


def upload_body_position_data(body_data: list[list]) -> None:

    # Positions list order [timestamp, distance_km, azimuth,
    #                       altitude, region_id, body_id,
    #                       constellation_id]

    with get_db_connection() as conn:

        cur = conn.cursor()

        q_str = """
                INSERT INTO body_assignment
                (at, distance_km, azimuth, altitude, region_id, body_id, constellation_id)
                VALUES
                %s"""

        execute_values(cur, q_str, body_data)


def upload_moon_phase_data(moon_phase_data: list[list]) -> None:

    for entry in moon_phase_data:
        for i in range(2):
            entry.append(None)
        entry.append("moon_phase")

    # Moon phase list order: [date, url, none, none, image_name]

    with get_db_connection() as conn:

        cur = conn.cursor()

        q_str = """
                INSERT INTO image
                (image_date, image_url, region_id, constellation_id, image_name)
                VALUES
                %s"""

        execute_values(cur, q_str, moon_phase_data)


def upload_astronomy_data(data_dict: list[dict]) -> None:

    position_data = data_dict["positions_list"]
    moon_data = data_dict["moon_phase_list"]

    upload_body_position_data(position_data)
    upload_moon_phase_data(moon_data)
