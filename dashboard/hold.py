import pandas as pd
import altair as alt
import streamlit as st
import numpy as np
from load_dashboard_data import load_average_cloud_coverage_by_region, connect_to_db
from dotenv import load_dotenv
import math

def calculate_starwatch_coefficient(body_distance, avg_visibility, avg_cloud_coverage, min_body_distance, max_body_distance):
    '''
    
    '''

    visibility_ratio = float(avg_visibility) / float(body_distance)

    log_visibility_ratio = math.log10(visibility_ratio)

    min_log = math.log10(float(avg_visibility) / float(max_body_distance))
    max_log = math.log10(float(avg_visibility) / float(min_body_distance))

    normalized_log_visibility_ratio = (log_visibility_ratio - min_log) / (max_log - min_log)

    starwatch_coefficient = 0.02 + normalized_log_visibility_ratio * (0.9 - 0.02)

    starwatch_coefficient *= (1 - float(avg_cloud_coverage) / 100)

    return starwatch_coefficient

if __name__ == '__main__':
    load_dotenv()
    connection_instance = connect_to_db()

    df = pd.DataFrame(load_average_cloud_coverage_by_region(connection_instance))

    df['date'] = pd.to_datetime(df['date']).dt.date  

    numeric_columns = ['distance_km', 'avg_vis', 'avg_cloud']
    df[numeric_columns] = df[numeric_columns].astype(float)

    st.write("Initial Data:")
    st.write(df.head(1000))

    unique_dates = df['date'].unique()
    selected_date = st.selectbox('Select Date:', unique_dates)

    available_regions = df[df['date'] == selected_date]['region_name'].unique()
    selected_region = st.selectbox('Select Region:', available_regions)

    filtered_df = df[(df['date'] == selected_date) & (df['region_name'] == selected_region)].copy()

    if filtered_df.empty:
        st.write("No data available for the selected date and region.")
    else:
        min_body_distance = filtered_df['distance_km'].min()
        max_body_distance = filtered_df['distance_km'].max()

        filtered_df['starwatch_coefficient'] = filtered_df.apply(
            lambda row: calculate_starwatch_coefficient(
                row['distance_km'],
                row['avg_vis'],  
                row['avg_cloud'],  
                min_body_distance,
                max_body_distance
            ), axis=1
        )

        st.write("Filtered Data with Starwatch Coefficient:")
        st.write(filtered_df.head(10))

        source = pd.DataFrame({
            'x': filtered_df['time'], 
            'y': filtered_df['body_name'],  
            'z': filtered_df['starwatch_coefficient']  
        })

        heatmap = alt.Chart(source).mark_rect().encode(
            x='x:O',
            y='y:O',
            color=alt.Color('z:Q', scale=alt.Scale(scheme='viridis'), title='Starwatch Coefficient')
        ).properties(
            title=f"Starwatch Coefficient Heatmap for {selected_region} on {selected_date}"
        )

        st.altair_chart(heatmap, use_container_width=True)
