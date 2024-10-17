'''Produces the skyplot for a given region at a given time'''
#pylint: disable=E0401,C0413,W0612,E1101,R0913
import sys
import os
from datetime import datetime as dt
from io import BytesIO
import tempfile
import matplotlib.pyplot as plt
from matplotlib import animation
import pandas as pd
import numpy as np
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'weekly-openmeteo')))
from extract import get_connection


def get_regions() -> list:
    '''Returns a list of all regions'''
    query = '''SELECT region_name FROM region'''
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            data = list(cur.fetchall())
    return data

def get_bodies() -> list:
    '''Returns a list of all bodies'''
    query = '''SELECT body_name FROM body'''
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            data = list(cur.fetchall())
    return data

def get_azimuth_data(region: str, time_point: dt):
    '''Uses psycopg2 to query the database for azimuth data for a given night'''
    query = '''SELECT b.body_name, ba.azimuth, ba.altitude,
    ba.distance_km, ba.at FROM region AS r
    JOIN body_assignment AS ba USING (region_id)
    JOIN body AS b USING (body_id)
    WHERE r.region_name = %s 
    AND ((DATE(ba.at) = %s AND EXTRACT(HOUR FROM ba.at) >= 12) OR 
    (DATE(ba.at) = DATE_ADD(%s, INTERVAL '1 DAY') AND EXTRACT(HOUR FROM ba.at) < 12))'''
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (region, time_point,time_point))
            data = cur.fetchall()
    return data


def transform_azimuth_data(data: list) -> pd.DataFrame:
    '''Transforms the azimuth data into a pandas dataframe'''
    df = pd.DataFrame(data)
    df.columns = ['body_name', 'azimuth', 'altitude', 'distance', 'time_point']
    df = df[df['altitude'] >= 0]
    df['azimuth'] = np.radians(df['azimuth'])
    df['altitude'] = 90 - df['altitude']
    return df


def sky_plot(celestial_df: pd.DataFrame, region: str, time_point) -> plt.subplot:
    '''Constructs the sky_plot using the celestial data'''
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={
                           'projection': 'polar'}, facecolor='black')
    ax.set_facecolor('black')
    body_properties_map = {'Sun': {'color': 'gold', 'size': 1391000},
                           'Moon': {'color': 'lightgray', 'size': 3474},
                           'Mars': {'color': 'red', 'size': 6779},
                           'Venus': {'color': 'yellow', 'size': 12104},
                           'Jupiter': {'color': 'orange', 'size': 139820},
                           'Saturn': {'color': 'khaki', 'size': 116460},
                           'Mercury': {'color': 'darkgray', 'size': 4880},
                           'Uranus': {'color': 'lightblue', 'size': 50724},
                           'Neptune': {'color': 'blue', 'size': 49244},
                           'Pluto': {'color': 'white', 'size': 2377}}

    unique_bodies = celestial_df['body_name'].unique()
    default_colors = plt.cm.plasma(np.linspace(0.2, 1, len(unique_bodies)))

    for i, body in enumerate(unique_bodies):
        if body not in body_properties_map:
            body_properties_map[body] = {
                'color': default_colors[i % len(default_colors)],
                'size': 500
            }

    first_time_point_df = celestial_df[celestial_df['time_point'] == time_point]
    sizes = first_time_point_df['body_name'].map(
        lambda x: body_properties_map[x]['size']).values
    sizes = np.interp(sizes, [min(prop['size'] for prop in body_properties_map.values()),
                              max(prop['size'] for prop in body_properties_map.values())],
                      [50, 1000])
    colors = first_time_point_df['body_name'].map(
        lambda x: body_properties_map[x]['color'])
    scatter = ax.scatter(first_time_point_df['azimuth'],
                         np.radians(first_time_point_df['altitude']),
                         s=sizes,
                         alpha=0.9, c=colors,
                         edgecolors='white')

    ax.set_xticks(np.radians(np.arange(0, 360, 30)))
    ax.set_xticklabels(np.arange(0, 360, 30), color='white')
    ax.set_ylim(0, np.pi / 2)
    ax.set_yticks(np.radians([0, 30, 60, 90]))
    ax.set_yticklabels(['90° (Zenith)', '60°', '30°',
                        '0° (Horizon)'], color='white')
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location('N')
    ax.grid(color='white', linestyle='-', linewidth=0.5)
    plt.title(f'Skyplot for {region} at {time_point.strftime("%d/%m/%Y %H:%M")}', color='white')
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color('white')
        spine.set_linewidth(1.5)

    return fig, ax, scatter, body_properties_map


def update_plot(frame, celestial_df, scatter, body_properties_map, text_elements, ax, region):
    '''Updates the skyplot with new data for each hour in the dataset'''
    time_point = frame
    current_df = celestial_df[celestial_df['time_point'] == time_point]
    sizes = current_df['body_name'].map(lambda x: body_properties_map[x]['size']).values
    sizes = np.interp(sizes, [min(prop['size'] for prop in body_properties_map.values()),
                    max(prop['size'] for prop in body_properties_map.values())], [50, 1000])

    colors = current_df['body_name'].map(lambda x: body_properties_map[x]['color'])

    scatter.set_offsets(np.c_[current_df['azimuth'],
                        np.radians(current_df['altitude'])])
    scatter.set_color(colors)
    scatter.set_sizes(sizes)

    for text in text_elements:
        text.remove()
    text_elements.clear()

    for i in range(len(current_df)):
        text = plt.text(current_df['azimuth'].iloc[i],
                        np.radians(current_df['altitude']).iloc[i],
                        current_df['body_name'].iloc[i],
                        fontsize=10, ha='right', va='bottom', color='white')
        text_elements.append(text)
    ax.set_title(f'Skyplot for {region} at {time_point.strftime("%d/%m/%Y %H:%M")}', color='white')


def animate_skyplot(celestial_df: pd.DataFrame, region: str):
    '''Animates the sky plot'''
    time_points = celestial_df['time_point'].unique()
    fig, ax, scatter, body_properties_map = sky_plot(
        celestial_df, region, time_points[0])
    text_elements = []
    ani = animation.FuncAnimation(fig, update_plot, frames=time_points,
                                  fargs=(celestial_df, scatter, body_properties_map,
                                         text_elements, ax, region),
                                  interval=1000, repeat=True)

    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmpfile:
        ani.save(tmpfile.name, writer='ffmpeg', fps=2)
        tmpfile.seek(0)
        video_path = tmpfile.name

    return video_path

def make_sky_plot(region: str, time: dt) -> plt.subplot:
    '''Orchestrates the pipeline to create the skyplot'''
    data = get_azimuth_data(region, time)
    clean_data = transform_azimuth_data(data)
    return animate_skyplot(clean_data, region)

def get_star_chart(body: str) -> str:
    '''Returns a string for a given body'''
    query = '''SELECT image_url, constellation_name FROM image
    JOIN constellation USING (constellation_id)
    JOIN body_assignment USING (constellation_id)
    JOIN body USING (body_id)
    WHERE body_name = %s AND
    image_date = CURRENT_DATE'''
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query,(body,))
            data = cur.fetchone()
    return data

if __name__ == '__main__':
    load_dotenv()
    make_sky_plot('Scotland', dt(2024, 10, 17, 0, 0, 0))
    print(get_star_chart('Venus'))
