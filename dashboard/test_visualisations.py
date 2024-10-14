from dashboard import connect_to_db

import pandas as pd
import altair as alt

conn = connect_to_db()

with conn: 
    with conn.cursor() as cur:
        query = """
        SELECT *
        FROM forecast
        WHERE at >= '2024-10-11 00:00:00' 
        AND at < '2024-10-12 00:00:00';
        """
        cur.execute(query)
        data = cur.fetchall()

        columns = [desc[0] for desc in cur.description]

df = pd.DataFrame(data, columns=columns)  # Specify column names
print(df.head())
