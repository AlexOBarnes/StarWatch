'''Contains code for stellarium page of dashboard'''
from datetime import datetime
import urllib
import streamlit as st

if __name__ == '__main__':
    st.markdown('''
    This dashboard provides an interactive view of the night sky as seen from **London**. The view updates automatically to reflect the current date and time.
    ''')

    # General coordinates for London, Liverpool street.
    DEFAULT_LATITUDE = 51.5074
    DEFAULT_LONGITUDE = -0.1278

    # Unless a specific location is provided, London used as a default.
    if 'latitude' not in st.session_state:
        st.session_state['latitude'] = DEFAULT_LATITUDE
    if 'longitude' not in st.session_state:
        st.session_state['longitude'] = DEFAULT_LONGITUDE

    def generate_stellarium_url(lat: str, lon: str, dt: datetime) -> str:
        '''
        Returns a stellarium URL to be used in an iFrame
        in the Streamlit dashboard.
        '''

        base_url = 'https://stellarium-web.org/'
        params = {
            'lat': lat,
            'lon': lon,
            'date': dt.strftime('%Y-%m-%d'),
            'time': dt.strftime('%H:%M')
        }
        query_string = urllib.parse.urlencode(params)
        full_url = f'{base_url}?{query_string}'
        return full_url

    def get_current_datetime() -> datetime:
        '''Returns the current time as a datetime object.'''
        return datetime.now()

    # The Stellarium iFrame is stored in a Streamlit container.
    with st.container():

        st.markdown('## Interactive Night Sky View')

        current_datetime = get_current_datetime()

        stellarium_url = generate_stellarium_url(
            DEFAULT_LATITUDE,
            DEFAULT_LONGITUDE,
            current_datetime
        )

        st.components.v1.html(f'''
        <iframe src='{stellarium_url}' style='width: 100%; height: 600px; border: none;'></iframe>
        ''', height=600)

        st.markdown(
            f'**Current Date & Time:** {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}')
