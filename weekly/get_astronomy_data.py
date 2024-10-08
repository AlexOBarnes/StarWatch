"""Calls from """

import json
from weekly.astronomy_request_functions import get_astronomy_all_body_positions, get_astronomy_one_body_position, get_astronomy_body_events
from weekly.astronomy_request_functions import get_star_chart, get_moon_phase


def save_to_file(data: dict, filename: str) -> None:
    """Save the data to a local .json file."""
    with open(filename, "w", encoding="utf-8") as f_obj:
        json.dump(data, f_obj, indent=4)


if __name__ == "__main__":

    #### ASTRONOMY API ####
    bodies_pos = get_astronomy_all_body_positions()
    save_to_file(bodies_pos, "astronomy_all_bodies.json")

    body_pos = get_astronomy_one_body_position()
    save_to_file(body_pos, "astronomy_one_body.json")

    body_events = get_astronomy_body_events()
    save_to_file(body_events, "body_events.json")

    star_chart = get_star_chart()
    print(star_chart)

    moon_phase = get_moon_phase()
    print(moon_phase)
