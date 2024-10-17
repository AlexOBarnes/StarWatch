'''Contains code for weather page of dashboard'''
import streamlit as st
import pandas as pd
import altair as alt
from load_dashboard_data import connect_to_db,load_forecasts_by_county_name


if __name__ == '__main__':
    st.title('⛅ Weather Data Dashboard 🌨️')

    conn = connect_to_db()
    # Loading all weather forecasts, joined by county ID to county names.
    data = load_forecasts_by_county_name(conn)

    df = pd.DataFrame(data)

    forecast_df = pd.DataFrame(data)

    # Ensuring there are no duplicate columns that can cause problems, as we joined on 'county_id'.
    forecast_df.columns = forecast_df.columns.str.replace(r'.1', '', regex=True)
    if forecast_df.columns.duplicated().any():
        forecast_df = forecast_df.loc[:, ~forecast_df.columns.duplicated()]

    forecast_df['at'] = pd.to_datetime(forecast_df['at'])

    # Extract just the date from the datetime for filtering purposes.
    forecast_df['date'] = forecast_df['at'].dt.date

    # Title of the weather page.
    st.title("Forecast Data Visualisation")

    county_names = forecast_df['county_name'].unique()
    selected_county = st.selectbox("Select County", county_names)

    # Let users select a date or date range for the forecast data.
    selected_dates = st.date_input(
        "Select Date or Date Range",
        [forecast_df['date'].min(), forecast_df['date'].max()]
    )

    # Initialise start_date and end_date, so the below if-clause holds.
    start_date = end_date = None

    # Check if the user selected only one date (i.e. they haven't picked an end date)
    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date, end_date = selected_dates
    elif isinstance(selected_dates, tuple) and len(selected_dates) == 1:
        # User only selected one date, show a clearer warning.
        st.warning(
            "Please select a valid start and end date for the visualisation date range.")
    else:
        start_date = end_date = selected_dates  # Single day selection

    if start_date and end_date:
        # Filter the forecast DataFrame based on the selected date(s) and county
        filtered_df = forecast_df[
            (forecast_df['date'] >= start_date) &
            (forecast_df['date'] <= end_date) &
            (forecast_df['county_name'] == selected_county)
        ]

        # A rolling average can only be applied if there's filtered data to apply it to.
        if not filtered_df.empty:
            # Apply rolling mean for smoother lines (adjust window size)
            filtered_df['cloud_coverage_rolling'] = filtered_df['cloud_coverage_percent'].rolling(
                window=24).mean()
            filtered_df['visibility_rolling'] = filtered_df['visibility_m'].rolling(
                window=24).mean()
            filtered_df['temperature_rolling'] = filtered_df['temperature_c'].rolling(
                window=24).mean()
            filtered_df['precipitation_prob_rolling'] = filtered_df['precipitation_probability_percent'].rolling(
                window=24).mean()
            filtered_df['precipitation_mm_rolling'] = filtered_df['precipitation_mm'].rolling(
                window=24).mean()

        # Check if a single day is selected
        is_single_day = start_date == end_date

        # The cloud coverage visualisation.
        cloud_chart = alt.Chart(filtered_df).mark_line().encode(
            x=alt.X('at:T', title='Time'),
            y=alt.Y('cloud_coverage_percent:Q', title='Cloud Coverage (%)'),
            tooltip=['at:T', 'cloud_coverage_percent']
        ).properties(
            width=1000,
            height=500,
            title='Cloud Coverage Over Time (Real vs. Rolling Average)'
        )

        # If it's a single day, add small points to the visualisation for clarity.
        if is_single_day:
            points = alt.Chart(filtered_df).mark_point(size=30, color="lightblue").encode(
                x='at:T',
                y='cloud_coverage_percent:Q',
                tooltip=['at:T', 'cloud_coverage_percent']
            )
            cloud_chart += points
        else:
            rolling_avg_line = alt.Chart(filtered_df).mark_line(color="white", opacity=0.28).encode(
                x='at:T',
                y=alt.Y('cloud_coverage_rolling:Q',
                        title='Cloud Coverage (%) (Rolling Average)'),
                tooltip=['at:T', 'cloud_coverage_rolling']
            )
            cloud_chart += rolling_avg_line

        # The visibility visualisation.
        visibility_chart = alt.Chart(filtered_df).mark_line(color="blue").encode(
            x=alt.X('at:T', title='Time'),
            y=alt.Y('visibility_m:Q', title='Visibility (m)',
                    scale=alt.Scale(type='log')),
            tooltip=['at:T', 'visibility_m']
        ).properties(
            width=1000,
            height=500,
            title='Visibility Over Time (Real vs. Rolling Average)'
        )

        if is_single_day:
            points = alt.Chart(filtered_df).mark_point(size=30, color="blue").encode(
                x='at:T',
                y='visibility_m:Q',
                tooltip=['at:T', 'visibility_m']
            )
            visibility_chart += points
        else:
            rolling_avg_line = alt.Chart(filtered_df).mark_line(color="white", opacity=0.28).encode(
                x='at:T',
                y=alt.Y('visibility_rolling:Q',
                        title='Visibility (m) (Rolling Average)'),
                tooltip=['at:T', 'visibility_rolling']
            )
            visibility_chart += rolling_avg_line

        # The temperature visualisation.
        temperature_chart = alt.Chart(filtered_df).mark_line(color="#D9372A").encode(
            x=alt.X('at:T', title='Time'),
            y=alt.Y('temperature_c:Q', title='Temperature (°C)'),
            tooltip=['at:T', 'temperature_c']
        ).properties(
            width=1000,
            height=500,
            title='Temperature Over Time (Real vs. Rolling Average)'
        )

        if is_single_day:
            points = alt.Chart(filtered_df).mark_point(size=30, color="#D9372A").encode(
                x='at:T',
                y='temperature_c:Q',
                tooltip=['at:T', 'temperature_c']
            )
            temperature_chart += points
        else:
            rolling_avg_line = alt.Chart(filtered_df).mark_line(color="white", opacity=0.28).encode(
                x='at:T',
                y=alt.Y('temperature_rolling:Q',
                        title='Temperature (°C) (Rolling Average)'),
                tooltip=['at:T', 'temperature_rolling']
            )
            temperature_chart += rolling_avg_line

        # Precipitation probability (%) and precipitation level (mm) visualisation.

        # Precipitation probability on the left y-axis
        precipitation_prob_chart = alt.Chart(filtered_df).mark_line(color='blue').encode(
            x=alt.X('at:T', title='Time'),
            y=alt.Y('precipitation_probability_percent:Q',
                    title='Precipitation Probability (%)'),
            tooltip=['at:T', 'precipitation_probability_percent']
        ).properties(
            width=1000,
            height=500
        )

        # Precipitation amount (mm) on the right y-axis.
        precipitation_mm_chart = alt.Chart(filtered_df).mark_line(color='green').encode(
            x=alt.X('at:T', title='Time'),
            y=alt.Y('precipitation_mm:Q', title='Precipitation (mm)'),
            tooltip=['at:T', 'precipitation_mm']
        )

        precipitation_chart = alt.layer(
            precipitation_prob_chart,
            precipitation_mm_chart
        ).resolve_scale(
            y='independent'
        ).properties(
            title="Precipitation Probability (%) and Precipitation (mm) Over Time"
        )

        col1, col2 = st.columns(2)
        # Display all charts in a single column
        with col1:
            st.altair_chart(cloud_chart, use_container_width=True)
            st.altair_chart(visibility_chart, use_container_width=True)

        with col2:
            st.altair_chart(temperature_chart, use_container_width=True)
            st.altair_chart(precipitation_chart, use_container_width=True)
