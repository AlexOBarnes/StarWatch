'''Produces the skyplot for a given region at a given time'''
#pylint: disable=E0401,C0413,W0612,E1101
import sys
import os
from datetime import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'weekly-openmeteo')))
from extract import get_connection


def get_azimuth_data(region: str, time_point:dt):
    '''Queries the database for azimuth data'''
    query = '''SELECT b.body_name, ba.azimuth, ba.altitude, ba.distance_km FROM region as r
    JOIN body_assignment as ba USING (region_id)
    JOIN body as b USING (body_id)
    WHERE r.region_name = %s AND
    ba.at = %s'''
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query,(region,time_point))
            data = cur.fetchall()

    return data


def transform_azimuth_data(data: list) -> pd.DataFrame:
    '''Processes the azimuth data and converts it to a pandas dataframe'''
    df = pd.DataFrame(data)
    df.columns = ['body_name', 'azimuth', 'altitude', 'distance']
    df = df[df['altitude'] >= 0]
    df['azimuth'] = np.radians(df['azimuth'])
    df['altitude'] = 90 - df['altitude']
    return df


def sky_plot(celestial_df: pd.DataFrame, region: str, time_point: dt) -> plt.subplot:
    '''Plots the azimuth and altitude data on a radial plot'''
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={
                           'projection': 'polar'}, facecolor='black')

    ax.set_facecolor('black')
    unique_bodies = celestial_df['body_name'].unique()
    colors = plt.cm.plasma(np.linspace(0.2, 1, len(unique_bodies)))
    body_color_map =  dict(zip(unique_bodies, colors))

    scatter = ax.scatter(celestial_df['azimuth'],
        np.radians(celestial_df['altitude']),alpha=0.9,
        c=celestial_df['body_name'].map(body_color_map),
        edgecolors='white')

    for i in range(len(celestial_df)):
        ax.text(celestial_df['azimuth'].iloc[i],
            np.radians(celestial_df['altitude']).iloc[i],
            celestial_df['body_name'].iloc[i],
            fontsize=10, ha='right', va='bottom', color='white')

    ax.set_xticks(np.radians(np.arange(0, 360, 30)))
    ax.set_xticklabels(np.arange(0, 360, 30), color='white')
    ax.set_ylim(0, np.pi / 2)
    ax.set_yticks(np.radians([0, 30, 60, 90]))
    ax.set_yticklabels(['90° (Zenith)', '60°', '30°','0° (Horizon)'],
                       color='white')
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location('N')
    ax.grid(color='white', linestyle='-', linewidth=0.5)
    plt.title(f'Skyplot for {region} at {time_point.strftime("%H:%M:%S on %d/%m/%Y")}',
              color='white')

    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color('white')
        spine.set_linewidth(1.5)
    plt.show()

def make_sky_plot(region:str,time:dt) -> plt.subplot:
    '''Runs script to make skyplot'''
    data = get_azimuth_data(region,time)
    clean_data = transform_azimuth_data(data)
    sky_plot(clean_data,region,time)


if __name__ == '__main__':
    load_dotenv()
    make_sky_plot('Scotland',dt(2024,10,26,20,0,0))
