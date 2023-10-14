import os
import psycopg2

from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
        host="localhost",
        database="cpsc535proj2",
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD'))

# Open a cursor to perform database operations
cur = conn.cursor()

# Activate PostGIS
cur.execute('CREATE EXTENSION IF NOT EXISTS postgis;')

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS blockages;')
cur.execute('CREATE TABLE blockages (id serial PRIMARY KEY,'
                                 'geog GEOGRAPHY(Point) UNIQUE NOT NULL,'
                                 'notes text NOT NULL DEFAULT \'\','
                                 'datetime_added timestamp DEFAULT CURRENT_TIMESTAMP);'
                                 )

# Insert dummy data into the table

# cur.execute('INSERT INTO blockages (geog, notes)'
#             'VALUES (%s, %s)',
#             ('POINT(-118.4079 33.9434)', 'Crash'))

conn.commit()

cur.close()
conn.close()