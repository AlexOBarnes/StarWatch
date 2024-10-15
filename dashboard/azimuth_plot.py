'''Produces the skyplot for a given region at a given time'''
#pylint: disable=E0401,C0413,W0612,E1101
import sys
import os
from datetime import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm
import pandas as pd
import numpy as np
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'weekly-openmeteo')))
from extract import get_connection


def get_azimuth_data(region: str, time_point:dt):
    '''Queries the database for azimuth data'''
    query = '''SELECT b.body_name, ba.azimuth, ba.altitude, ba.distance_km,ba.at FROM region as r
    JOIN body_assignment as ba USING (region_id)
    JOIN body as b USING (body_id)
    WHERE r.region_name = %s AND
    DATE(ba.at) = %s'''
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query,(region,time_point))
            data = cur.fetchall()

    return data


def transform_azimuth_data(data: list) -> pd.DataFrame:
    '''Processes the azimuth data and converts it to a pandas dataframe'''
    df = pd.DataFrame(data)
    df.columns = ['body_name', 'azimuth', 'altitude', 'distance','time_point']
    df = df[df['altitude'] >= 0]
    df['azimuth'] = np.radians(df['azimuth'])
    df['altitude'] = 90 - df['altitude']
    return df


def sky_plot(celestial_df: pd.DataFrame, region: str, time_point) -> plt.subplot:
    '''Plots the azimuth and altitude data on a radial plot'''
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={
                           'projection': 'polar'}, facecolor='black')

    ax.set_facecolor('black')
    unique_bodies = celestial_df['body_name'].unique()
    colors = cm.plasma(np.linspace(0.2, 1, len(unique_bodies)))
    body_color_map = dict(zip(unique_bodies, colors))

    scatter = ax.scatter([], [], alpha=0.9, edgecolors='white')
    ax.set_xticks(np.radians(np.arange(0, 360, 30)))
    ax.set_xticklabels(np.arange(0, 360, 30), color='white')
    ax.set_ylim(0, np.pi / 2)
    ax.set_yticks(np.radians([0, 30, 60, 90]))
    ax.set_yticklabels(['90° (Zenith)', '60°', '30°',
                       '0° (Horizon)'], color='white')
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location('N')
    ax.grid(color='white', linestyle='-', linewidth=0.5)

    plt.title(f'Skyplot for {region} at {time_point}', color='white')

    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color('white')
        spine.set_linewidth(1.5)

    return fig, ax, scatter, body_color_map


def update_plot(frame, celestial_df, scatter, body_color_map, ax, region):
    time_point = frame
    current_df = celestial_df[celestial_df['time_point'] == time_point]
    scatter.set_offsets(np.c_[current_df['azimuth'],
                        np.radians(current_df['altitude'])])
    scatter.set_color(current_df['body_name'].map(body_color_map))
    ax.clear()
    for i in range(len(current_df)):
        ax.text(current_df['azimuth'].iloc[i],
                np.radians(current_df['altitude']).iloc[i],
                current_df['body_name'].iloc[i],
                fontsize=10, ha='right', va='bottom', color='white')
    ax.set_xticks(np.radians(np.arange(0, 360, 30)))
    ax.set_xticklabels(np.arange(0, 360, 30), color='white')
    ax.set_ylim(0, np.pi / 2)
    ax.set_yticks(np.radians([0, 30, 60, 90]))
    ax.set_yticklabels(['90° (Zenith)', '60°', '30°',
                       '0° (Horizon)'], color='white')
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location('N')
    ax.grid(color='white', linestyle='-', linewidth=0.5)
    plt.title(f'Skyplot for {region} at {time_point.strftime(
        "%H:%M:%S on %d/%m/%Y")}', color='white')


def animate_skyplot(celestial_df: pd.DataFrame, region: str):
    time_points = celestial_df['time_point'].unique()
    fig, ax, scatter, body_color_map = sky_plot(
        celestial_df, region, time_points[0])
    ani = animation.FuncAnimation(fig, update_plot, frames=time_points,
                                  fargs=(celestial_df, scatter,
                                         body_color_map, ax, region),
                                  interval=1000, repeat=True)

    plt.show()

def make_sky_plot(region:str,time:dt) -> plt.subplot:
    '''Runs script to make skyplot'''
    data = get_azimuth_data(region,time)
    clean_data = transform_azimuth_data(data)
    print(clean_data)
    animate_skyplot(clean_data, 'My Region')


if __name__ == '__main__':
    load_dotenv()
    make_sky_plot('Scotland',dt(2024,10,26,0,0,0))
