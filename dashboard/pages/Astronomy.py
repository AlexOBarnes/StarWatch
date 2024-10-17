'''Contains code for astronomy page of dashboard'''
from datetime import datetime, date
import streamlit as st
from aurora_map import create_body_visibility_map
from azimuth_plot import make_sky_plot, get_bodies, get_star_chart, get_regions


if __name__ == '__main__':
    bodies = [body[0] for body in get_bodies()]
    selected_body = st.selectbox("Select body", bodies)
    col1, col2 = st.columns(2)
    with col1:
        st.header(f'{selected_body} Visibility Across The UK')
        body_visibility = create_body_visibility_map(selected_body)
        if body_visibility:
            st.pyplot(body_visibility)
        else:
            st.write('Body map not available right now. Sorry for the inconvenience')
    with col2:
        st.header(f'{selected_body} star chart')
        starchart, constellation = get_star_chart(selected_body)
        if starchart:
            st.write(f'Tonight {selected_body} will be visible in the {
                        constellation} constellation.')
            st.image(starchart)
        else:
            st.write('No star chart is available for this celestial body tonight')

    regions = [region[0] for region in get_regions()]
    region = st.selectbox("Select region", regions)
    selected_date = st.date_input(
        "Select a date:",
        value=date.today(),
        min_value=date(2024, 10, 7),
        max_value=date(2100, 12, 31)
    )
    col1, col2 = st.columns(2)
    with col1:
        st.header('What has been visible in your region?')
        st.write(
            'Historical data heat map to be implemented. Sorry for the inconvenience.')
    with col2:
        animation_data = make_sky_plot(
            region, datetime.combine(selected_date, datetime.min.time()))
        st.header(f'Skyplot for {region} on {datetime.combine(
            selected_date, datetime.min.time()).strftime('%d/%m/%y')} ')
        if animation_data:
            st.video(animation_data, format='.mp4')
        else:
            st.write('No skyplot is available for this region on this date')
