'''File to generate maps for the dashboard.'''

from os import environ as ENV

import geopandas as gpd
import matplotlib.pyplot as plt
from psycopg2 import connect, extensions, extras
from dotenv import load_dotenv


COUNTY_MAPPING = {
    "Hartlepool": "County Durham", "Middlesbrough": "North Yorkshire",
    "Redcar and Cleveland": "North Yorkshire", "Stockton-on-Tees": "County Durham",
    "Darlington": "County Durham", "Halton": "Cheshire",
    "Warrington": "Cheshire", "Blackburn with Darwen": "Lancashire",
    "Blackpool": "Lancashire", "Kingston upon Hull, City of": "East Riding of Yorkshire",
    "East Riding of Yorkshire": "East Riding of Yorkshire",
    "North East Lincolnshire": "Lincolnshire",
    "North Lincolnshire": "Lincolnshire", "York": "North Yorkshire",
    "Derby": "Derbyshire", "Leicester": "Leicestershire",
    "Rutland": "Rutland", "Nottingham": "Nottinghamshire",
    "Herefordshire, County of": "Herefordshire", "Telford and Wrekin": "Shropshire",
    "Stoke-on-Trent": "Staffordshire", "Bath and North East Somerset": "Somerset",
    "Bristol, City of": "Bristol", "North Somerset": "Somerset",
    "South Gloucestershire": "Gloucestershire", "Plymouth": "Devon", "Torbay": "Devon",
    "Swindon": "Wiltshire", "Peterborough": "Cambridgeshire",
    "Luton": "Bedfordshire", "Southend-on-Sea": "Essex",
    "Thurrock": "Essex", "Medway": "Kent",
    "Bracknell Forest": "Berkshire", "West Berkshire": "Berkshire",
    "Reading": "Berkshire", "Slough": "Berkshire",
    "Windsor and Maidenhead": "Berkshire", "Wokingham": "Berkshire",
    "Milton Keynes": "Buckinghamshire", "Brighton and Hove": "East Sussex",
    "Portsmouth": "Hampshire", "Southampton": "Hampshire",
    "Isle of Wight": "Hampshire", "County Durham": "County Durham",
    "Cheshire East": "Cheshire", "Cheshire West and Chester": "Cheshire",
    "Shropshire": "Shropshire", "Cornwall": "Cornwall",
    "Isles of Scilly": "Cornwall", "Wiltshire": "Wiltshire",
    "Bedford": "Bedfordshire", "Central Bedfordshire": "Bedfordshire",
    "Northumberland": "Northumberland", "Bournemouth, Christchurch and Poole": "Dorset",
    "Dorset": "Dorset", "Buckinghamshire": "Buckinghamshire",
    "North Northamptonshire": "Northamptonshire", "West Northamptonshire": "Northamptonshire",
    "Cumberland": "Cumbria", "Westmorland and Furness": "Cumbria",
    "North Yorkshire": "North Yorkshire", "Somerset": "Somerset",
    "Bolton": "Greater Manchester", "Bury": "Greater Manchester",
    "Manchester": "Greater Manchester", "Oldham": "Greater Manchester",
    "Rochdale": "Greater Manchester", "Salford": "Greater Manchester",
    "Stockport": "Greater Manchester", "Tameside": "Greater Manchester",
    "Trafford": "Greater Manchester", "Wigan": "Greater Manchester",
    "Knowsley": "Merseyside", "Liverpool": "Merseyside",
    "St. Helens": "Merseyside", "Sefton": "Merseyside",
    "Wirral": "Merseyside", "Barnsley": "South Yorkshire",
    "Doncaster": "South Yorkshire", "Rotherham": "South Yorkshire",
    "Sheffield": "South Yorkshire", "Newcastle upon Tyne": "Tyne and Wear",
    "North Tyneside": "Tyne and Wear", "South Tyneside": "Tyne and Wear",
    "Sunderland": "Tyne and Wear", "Birmingham": "West Midlands",
    "Coventry": "West Midlands", "Dudley": "West Midlands",
    "Sandwell": "West Midlands", "Solihull": "West Midlands",
    "Walsall": "West Midlands", "Wolverhampton": "West Midlands",
    "Bradford": "West Yorkshire", "Calderdale": "West Yorkshire",
    "Kirklees": "West Yorkshire", "Leeds": "West Yorkshire",
    "Wakefield": "West Yorkshire", "Gateshead": "Tyne and Wear",
    "City of London": "Greater London", "Barking and Dagenham": "Greater London",
    "Barnet": "Greater London", "Bexley": "Greater London",
    "Brent": "Greater London", "Bromley": "Greater London",
    "Camden": "Greater London", "Croydon": "Greater London",
    "Ealing": "Greater London", "Enfield": "Greater London",
    "Greenwich": "Greater London", "Hackney": "Greater London",
    "Hammersmith and Fulham": "Greater London", "Haringey": "Greater London",
    "Harrow": "Greater London", "Havering": "Greater London",
    "Hillingdon": "Greater London", "Hounslow": "Greater London",
    "Islington": "Greater London", "Kensington and Chelsea": "Greater London",
    "Kingston upon Thames": "Greater London", "Lambeth": "Greater London",
    "Lewisham": "Greater London", "Merton": "Greater London",
    "Newham": "Greater London", "Redbridge": "Greater London",
    "Richmond upon Thames": "Greater London", "Southwark": "Greater London",
    "Sutton": "Greater London", "Tower Hamlets": "Greater London",
    "Waltham Forest": "Greater London", "Wandsworth": "Greater London",
    "Westminster": "Greater London", "Cambridgeshire": "Cambridgeshire",
    "Derbyshire": "Derbyshire", "Devon": "Devon",
    "East Sussex": "East Sussex", "Essex": "Essex",
    "Gloucestershire": "Gloucestershire", "Hampshire": "Hampshire",
    "Hertfordshire": "Hertfordshire", "Kent": "Kent",
    "Lancashire": "Lancashire", "Leicestershire": "Leicestershire",
    "Lincolnshire": "Lincolnshire", "Norfolk": "Norfolk",
    "Nottinghamshire": "Nottinghamshire", "Oxfordshire": "Oxfordshire",
    "Staffordshire": "Staffordshire", "Suffolk": "Suffolk",
    "Surrey": "Surrey", "Warwickshire": "Warwickshire",
    "West Sussex": "West Sussex", "Worcestershire": "Worcestershire",
    "Antrim and Newtownabbey": "Antrim", "Armagh City, Banbridge and Craigavon": "Armagh",
    "Belfast": "Antrim", "Causeway Coast and Glens": "Londonderry",
    "Derry City and Strabane": "Londonderry", "Fermanagh and Omagh": "Fermanagh",
    "Lisburn and Castlereagh": "Antrim", "Mid and East Antrim": "Antrim",
    "Mid Ulster": "Tyrone", "Newry, Mourne and Down": "Down",
    "Ards and North Down": "Down", "Clackmannanshire": "Clackmannanshire",
    "Dumfries and Galloway": "Dumfries and Galloway", "East Ayrshire": "East Ayrshire",
    "East Lothian": "East Lothian", "East Renfrewshire": "East Renfrewshire",
    "Na h-Eileanan Siar": "Western Isles", "Falkirk": "Falkirk",
    "Highland": "Highland", "Inverclyde": "Inverclyde",
    "Midlothian": "Midlothian", "Moray": "Moray",
    "North Ayrshire": "North Ayrshire", "Orkney Islands": "Orkney Islands",
    "Scottish Borders": "Scottish Borders", "Shetland Islands": "Shetland Islands",
    "South Ayrshire": "South Ayrshire", "South Lanarkshire": "South Lanarkshire",
    "Stirling": "Stirling", "Aberdeen City": "Aberdeen City",
    "Aberdeenshire": "Aberdeenshire", "Argyll and Bute": "Argyll and Bute",
    "City of Edinburgh": "Edinburgh", "Renfrewshire": "Renfrewshire",
    "West Dunbartonshire": "West Dunbartonshire",
    "West Lothian": "West Lothian", "Angus": "Angus",
    "Dundee City": "Dundee City", "East Dunbartonshire": "East Dunbartonshire",
    "Fife": "Fife", "Perth and Kinross": "Perth and Kinross",
    "Glasgow City": "Glasgow City", "North Lanarkshire": "North Lanarkshire",
    "Isle of Anglesey": "Anglesey", "Gwynedd": "Gwynedd",
    "Conwy": "Conwy", "Denbighshire": "Denbighshire",
    "Flintshire": "Flintshire", "Wrexham": "Wrexham",
    "Ceredigion": "Ceredigion", "Pembrokeshire": "Pembrokeshire",
    "Carmarthenshire": "Carmarthenshire", "Swansea": "Swansea",
    "Neath Port Talbot": "Neath Port Talbot", "Bridgend": "Bridgend",
    "Vale of Glamorgan": "Vale of Glamorgan", "Cardiff": "Cardiff",
    "Rhondda Cynon Taf": "Rhondda Cynon Taf", "Caerphilly": "Caerphilly",
    "Blaenau Gwent": "Blaenau Gwent", "Torfaen": "Torfaen",
    "Monmouthshire": "Monmouthshire", "Newport": "Newport",
    "Powys": "Powys", "Merthyr Tydfil": "Merthyr Tydfil"
}

NORTHERN_REGIONS = ['Scotland', 'North East (England)', 'North West (England)',
                    'Yorkshire and The Humber', 'Northern Ireland']


def get_connection() -> extensions.connection:
    '''Returns a psycopg2 connection given the loaded environment variables.'''
    load_dotenv()

    return connect(f'''dbname={ENV["DB_NAME"]} user={ENV["DB_USER"]}
                 host={ENV["DB_HOST"]} password={ENV["DB_PASSWORD"]} port={ENV["DB_PORT"]}''')


def get_aurora_data() -> str:
    '''Returns a string of the current aurora alert level.'''
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


def get_cloud_data() -> dict:
    '''Returns a dict of all counties cloud coverage for the current time and day.'''
    query = '''SELECT c.county_name, f.cloud_coverage_percent
            FROM county AS c JOIN forecast AS f USING (county_id)
            WHERE EXTRACT(HOUR FROM f.at) = EXTRACT(HOUR FROM CURRENT_TIMESTAMP)
            AND DATE(f.at) = DATE(CURRENT_TIMESTAMP);'''

    with get_connection() as conn:
        with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            cur.execute(query)
            result = cur.fetchall()

    return {row['county_name']: row['cloud_coverage_percent'] for row in result}


def map_cloud_coverage() -> dict:
    '''Return a dict that has all the counties in the shape file mapped to the
    counties from the shape file.'''
    cloud_cov = get_cloud_data()

    mapped_values = {}
    for area, county in COUNTY_MAPPING.items():
        if county in cloud_cov:
            mapped_values[area] = cloud_cov[county] / 100

    return mapped_values


def map_region_colours(map_regions: list[str]) -> dict:
    '''Returns a dict of the regions mapped to a colour for aurora possibility.'''
    colour = get_aurora_data()

    if colour == 'Green':
        colours = {region: 'red' for region in map_regions}
    elif colour == 'Yellow':
        colours = {
            region: 'red' for region in map_regions if region not in NORTHERN_REGIONS}
        for region in NORTHERN_REGIONS:
            colours[region] = 'blue'
    elif colour == 'Amber':
        colours = {
            region: 'blue' for region in map_regions if region not in NORTHERN_REGIONS}
        for region in NORTHERN_REGIONS:
            colours[region] = 'green'
    else:
        colours = {region: 'green' for region in map_regions}

    return colours


def create_aurora_map() -> plt.figure:
    '''Returns a map figure showing the possibility of an aurora sighting per region
    for the current time, over-layed with a map of each counties current cloud
    coverage as a white alpha value.'''
    fig, ax = plt.subplots(figsize=(5, 5))

    gdf1 = gpd.read_file("shapefile/NUTS1_Jan_2018_UGCB_in_the_UK.shp")
    region_colours = map_region_colours(gdf1.nuts118nm.tolist())
    gdf1['color'] = gdf1['nuts118nm'].map(region_colours)
    gdf1.plot(color=gdf1['color'], edgecolor='black', linewidth=1, ax=ax)

    gdf2 = gpd.read_file("shapefile/CTYUA_DEC_2023_UK_BGC.shp")
    mapped_values = map_cloud_coverage()
    gdf2['alpha'] = gdf2['CTYUA23NM'].map(mapped_values)
    gdf2.plot(ax=ax, color='white', alpha=gdf2['alpha'],  edgecolor='none')

    legend_text = '''- Green: Likely to see aurora.
    - Orange: Possible to see aurora.
    - Red: Unlikely to see aurora.

    White overlay opacity indicates
    current cloud coverage.'''

    props = {'boxstyle': 'round', 'facecolor': 'white', 'alpha': 0.5}
    ax.text(1.6, 0.8, legend_text, fontsize=6, bbox=props,
            transform=ax.transAxes, verticalalignment='top', horizontalalignment='right')

    ax.set_axis_off()
    plt.gcf().set_facecolor('black')

    return fig


def get_average_cloud_data() -> dict:
    '''Returns a dict of all counties average cloud coverage for the night 1700-0500.'''
    query = """SELECT c.county_name,
    AVG(f.cloud_coverage_percent) AS avg_cloud_cov
    FROM county AS c
    JOIN forecast AS f USING (county_id)
    WHERE ((DATE(f.at) = DATE(CURRENT_TIMESTAMP)
    AND EXTRACT(HOUR FROM f.at) >= 17)
    OR (DATE(f.at) = DATE(CURRENT_TIMESTAMP + INTERVAL '1 day')
    AND EXTRACT(HOUR FROM f.at) <= 05))
    GROUP BY c.county_name;"""

    with get_connection() as conn:
        with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            cur.execute(query)
            result = cur.fetchall()

    return {row['county_name']: float(row['avg_cloud_cov']) for row in result}


def get_body_visible_regions(body: str) -> list[str]:
    '''Returns a list of regions that will have a given body appear at some
    point over the night period 1700-0500'''
    query = """SELECT DISTINCT r.region_name
    FROM region AS r
    JOIN body_assignment AS ba USING(region_id)
    JOIN body AS b USING(body_id)
    WHERE b.body_name = %s
    AND ((DATE(ba.at) = DATE(CURRENT_TIMESTAMP)
    AND EXTRACT(HOUR FROM ba.at) >= 17)
    OR (DATE(ba.at) = DATE(CURRENT_TIMESTAMP + INTERVAL '1 day')
    AND EXTRACT(HOUR FROM ba.at) <= 05))
    AND ba.altitude > 5.0;"""

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (body.title(), ))
            results = [region[0] for region in cur.fetchall()]

    return results


def map_body_visibility_regions_colours(body: str, map_regions: list) -> dict:
    '''Returns a dict with each region as keys and values either green if the body
    is able to be seen in the night, and red if not.'''
    visible_regions = get_body_visible_regions(body)

    region_colours = {}

    for region in map_regions:
        if region in visible_regions:
            region_colours[region] = 'green'
        else:
            region_colours[region] = 'red'

    return region_colours


def map_average_cloud_coverage() -> dict:
    '''Return a dict that has all the counties in the shape file mapped to the
    counties from the shape file.'''
    avg_cloud_cov = get_average_cloud_data()

    mapped_values = {}
    for area, county in COUNTY_MAPPING.items():
        if county in avg_cloud_cov:
            mapped_values[area] = avg_cloud_cov[county] / 100

    return mapped_values


def create_body_visibility_map(body: str) -> plt.Figure:
    '''Returns a map figure showing whether a given body will be
    visible for that night, over-layed with the average cloud coverage
    for the night for each county.'''
    fig, ax = plt.subplots(figsize=(5, 5))

    gdf1 = gpd.read_file("shapefile/NUTS1_Jan_2018_UGCB_in_the_UK.shp")
    region_colours = map_body_visibility_regions_colours(
        body, gdf1.nuts118nm.tolist())
    gdf1['color'] = gdf1['nuts118nm'].map(region_colours)
    gdf1.plot(color=gdf1['color'], edgecolor='black', linewidth=1, ax=ax)

    gdf2 = gpd.read_file("shapefile/CTYUA_DEC_2023_UK_BGC.shp")
    mapped_values = map_average_cloud_coverage()
    gdf2['alpha'] = gdf2['CTYUA23NM'].map(mapped_values)
    gdf2.plot(ax=ax, color='white', alpha=gdf2['alpha'],  edgecolor='none')

    legend_text = f'''- Green: {body} is visible tonight.
    - Red: {body} is not visible tonight.

    White overlay opacity indicates
    average cloud coverage tonight.'''

    props = {'boxstyle': 'round', 'facecolor': 'white', 'alpha': 0.5}
    ax.text(1.6, 0.8, legend_text, fontsize=6, bbox=props,
            transform=ax.transAxes, verticalalignment='top', horizontalalignment='right')

    ax.set_axis_off()
    plt.gcf().set_facecolor('black')

    return fig


def get_average_visibility_data() -> dict:
    '''Returns a dict of all counties average visibility 
    in meters for the night 1700-0500.'''
    query = """SELECT c.county_name,
    AVG(f.visibility_m) AS avg_vis
    FROM county AS c
    JOIN forecast AS f USING (county_id)
    WHERE ((DATE(f.at) = DATE(CURRENT_TIMESTAMP)
    AND EXTRACT(HOUR FROM f.at) >= 17)
    OR (DATE(f.at) = DATE(CURRENT_TIMESTAMP + INTERVAL '1 day')
    AND EXTRACT(HOUR FROM f.at) <= 05))
    GROUP BY c.county_name;"""

    with get_connection() as conn:
        with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            cur.execute(query)
            result = cur.fetchall()

    return {row['county_name']: int(row['avg_vis']) for row in result}


def map_average_visibility_colour() -> dict:
    '''Return a dict that has all the counties in the shape file mapped to the
    counties from the shape file.'''
    avg_visibility = get_average_visibility_data()

    mapped_values = {}
    for area, county in COUNTY_MAPPING.items():
        if county in avg_visibility:
            if avg_visibility[county] < 5000:
                mapped_values[area] = 'gray'
                continue
            if avg_visibility[county] < 10000:
                mapped_values[area] = 'green'
                continue
            if avg_visibility[county] < 20000:
                mapped_values[area] = 'blue'
                continue
            if avg_visibility[county] < 40000:
                mapped_values[area] = 'purple'
                continue
            mapped_values[area] = 'gold'

    return mapped_values


def create_visibility_map() -> plt.Figure:
    '''Returns a map figure showing the general visibility and cloud coverage
    for the current night.'''
    fig, ax = plt.subplots(figsize=(5, 5))

    gdf1 = gpd.read_file("shapefile/CTYUA_DEC_2023_UK_BGC.shp")
    mapped_values = map_average_visibility_colour()
    gdf1['color'] = gdf1['CTYUA23NM'].map(mapped_values)
    gdf1.plot(color=gdf1['color'], edgecolor='black', linewidth=1, ax=ax)

    gdf2 = gpd.read_file("shapefile/CTYUA_DEC_2023_UK_BGC.shp")
    mapped_values = map_average_cloud_coverage()
    gdf2['alpha'] = gdf2['CTYUA23NM'].map(mapped_values)
    gdf2.plot(ax=ax, color='white', alpha=gdf2['alpha'],  edgecolor='none')

    legend_text = '''- Grey: Visibility below 5km.
    - Green: Visibility between 5km and 10km.
    - Blue: Visibility between 10km and 20km.
    - Purple: Visibility between 20km and 40km.
    - Gold: Visibility above 40km.

    White overlay opacity indicates 
    average cloud coverage tonight.'''

    props = {'boxstyle': 'round', 'facecolor': 'white', 'alpha': 0.5}
    ax.text(1.6, 0.8, legend_text, fontsize=6, bbox=props,
            transform=ax.transAxes, verticalalignment='top', horizontalalignment='right')

    ax.set_axis_off()
    plt.gcf().set_facecolor('black')

    return fig


if __name__ == "__main__":
    aurora_map = create_aurora_map()
    plt.show()

    body_visibility_map = create_body_visibility_map('Jupiter')
    plt.show()

    average_visibility_map = create_visibility_map()
    plt.show()
