import geopandas as gpd
import matplotlib.pyplot as plt
from psycopg2 import connect, extensions
from dotenv import load_dotenv
from os import environ as ENV


def get_connection() -> extensions.connection:
    '''Returns a psycopg2 connection given the loaded environment variables.'''
    load_dotenv()

    return connect(f'''dbname={ENV["DB_NAME"]} user={ENV["DB_USER"]}
                 host={ENV["DB_HOST"]} password={ENV["DB_PASSWORD"]} port={ENV["DB_PORT"]}''')


def get_aurora_data() -> str:
    ''''''
    query = '''SELECT ac.colour FROM aurora_alert AS aa 
            JOIN aurora_colour AS ac 
            USING (aurora_colour_id) 
            ORDER BY aa.alert_time DESC 
            LIMIT 1;'''

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchone()[0]

    return result


if __name__ == "__main__":
    northern_regions = ['Scotland',
                        'North East (England)', 'North West (England)',
                        'Yorkshire and The Humber', 'Northern Ireland']

    # colour = get_aurora_data()
    colour = 'Amber'

    # Load the shapefile
    gdf = gpd.read_file("shapefile/NUTS1_Jan_2018_UGCB_in_the_UK.shp")

    if colour == 'Green':
        colours = {key: 'green' for key in gdf.nuts118nm}

    elif colour == 'Yellow':
        colours = {
            key: 'green' for key in gdf.nuts118nm if key not in northern_regions}
        for region in northern_regions:
            colours[region] = 'yellow'

    elif colour == 'Amber':
        colours = {
            key: 'yellow' for key in gdf.nuts118nm if key not in northern_regions}
        for region in northern_regions:
            colours[region] = 'orange'

    else:
        colours = {key: 'orange' for key in gdf.nuts118nm}

    # Create a color column based on the region names
    gdf['color'] = gdf['nuts118nm'].map(colours)

    # Plot the map with specific region colors
    ax = gdf.plot(color=gdf['color'], edgecolor='black',
                  linewidth=0.5)
    ax.set_axis_off()
    plt.title('Possible Aurora Sightings')
    plt.show()
