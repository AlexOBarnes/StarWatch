import streamlit as st
from datetime import datetime
import urllib.parse
from streamlit_autorefresh import st_autorefresh


st.title("⭐ Starwatch Data Dashboard ⭐")


st.markdown("""
This dashboard provides an interactive view of the night sky as seen from **Liverpool Street, London**. The view updates automatically to reflect the current date and time.
""")

# Default Coordinates for Liverpool Street, London from Google Maps.
DEFAULT_LATITUDE = 51.5171
DEFAULT_LONGITUDE = -0.0822


def generate_stellarium_url(lat, lon, dt):
    base_url = "https://stellarium-web.org/"
    params = {
        "lat": lat,
        "lon": lon,
        "date": dt.strftime("%Y-%m-%d"),
        "time": dt.strftime("%H:%M")
    }
    query_string = urllib.parse.urlencode(params)
    full_url = f"{base_url}?{query_string}"
    return full_url


def get_current_datetime():
    return datetime.now()


refresh_interval = 60  

st_autorefresh(interval=refresh_interval * 1000, limit=None, key="auto_refresh")

with st.expander("⚙️ Settings", expanded=False):
    st.markdown("### Location Settings")
    
    latitude = st.number_input(
        "Latitude",
        value=DEFAULT_LATITUDE,
        format="%.4f",
        help="Enter the latitude of your location (-90 to 90).",
        min_value=-90.0,
        max_value=90.0,
        step=0.0001
    )
    
    longitude = st.number_input(
        "Longitude",
        value=DEFAULT_LONGITUDE,
        format="%.4f",
        help="Enter the longitude of your location (-180 to 180).",
        min_value=-180.0,
        max_value=180.0,
        step=0.0001
    )
    

    if st.button("Reset to Default"):
        st.session_state["latitude"] = DEFAULT_LATITUDE
        st.session_state["longitude"] = DEFAULT_LONGITUDE


with st.container():
    st.markdown("## Interactive Night Sky View")
    

    current_datetime = get_current_datetime()
    

    stellarium_url = generate_stellarium_url(latitude, longitude, current_datetime)
    

    st.components.v1.html(f"""
    <style>
        iframe {{
            width: 100%;
            height: 600px;
            border: none;
        }}
        iframe {{
            zoom: 1.25;  /* Adjust zoom as needed */
        }}
    </style>
    <iframe src="{stellarium_url}" scrolling="no"></iframe>
    <script>
        document.querySelector('iframe').onload = function() {{
            const iframeDoc = this.contentDocument || this.contentWindow.document;
            iframeDoc.querySelector('aside').style.display = 'none';  // Hides the left menu
        }};
    </script>
    """, height=600)


    st.markdown(f"**Current Date & Time:** {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}")


st.markdown("""
---
*This dashboard automatically updates every minute to provide the most current view of the night sky.*
""")