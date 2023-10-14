import os
import psycopg2
import json
import datetime
from shapely import wkb
import pandas as pd
import geopandas as gpd

from dotenv import load_dotenv

import flask
from flask import request
from flask_restful import Resource, Api
from flask_cors import CORS

from services import run_simulation, get_shortest_paths

load_dotenv()

app = flask.Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


# DB connection
def get_db_connection():
    conn = psycopg2.connect(host="localhost",
                            database="cpsc535proj2",
                            user=os.getenv("DB_USERNAME"),
                            password=os.getenv("DB_PASSWORD"))
    return conn

# helper to object turn into json
class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


class Home(Resource):
    def get(self):
        data = {
            "message" : "Hello! API is running!"
        }

        return {
            "data": data,
        }


class Blockages(Resource):
    # get all blockages within a certain rectangle bound
    def get(self):
        conn = get_db_connection()
        cur = conn.cursor()

        args = request.args
        xmin = args['xmin']
        ymin = args['ymin']
        xmax = args['xmax']
        ymax = args['ymax']

        cur.execute("""
            SELECT *
            FROM   blockages
            WHERE  ST_GeomFromText(ST_AsText(geog)) @
                ST_MakeEnvelope (
                    %s, %s,     -- bounding 
                    %s, %s,     -- box limits
                    4326)       -- SRID for leaflet and OMS
        """, (str(xmin), str(ymin), str(xmax), str(ymax)))
        blockages = cur.fetchall()

        # convert to dict
        # make dict
        results = []
        for row in blockages:
            row_dict = {}
            row_dict["id"] = row[0]
            row_dict["geog_wkb"] = row[1]
            row_dict["notes"] = row[2]
            row_dict["datetime_added"] = row[3].isoformat()

            # convert wkb to lat long
            point = wkb.loads(row[1])
            row_dict["lng"] = point.x
            row_dict["lat"] = point.y

            results.append(row_dict)

        cur.close()
        conn.close()

        return {
            "data": results,
            "status": "SUCCESS",
        }


    # add a blockage
    def post(self):
        conn = get_db_connection()
        cur = conn.cursor()

        json_data = request.get_json(force=True)
        lat = json_data['lat']
        lng = json_data['lng']

        cur.execute("""
            WITH ins AS (
               INSERT INTO blockages (geog)
               VALUES ('POINT(%s %s)')
               ON CONFLICT (geog) DO UPDATE
               SET    geog = NULL
               WHERE  FALSE      -- never executed, but locks the row
               RETURNING id
               )
            SELECT id FROM ins
            UNION  ALL
            SELECT id FROM blockages 
            WHERE  geog = 'POINT(%s %s)'  -- only executed if no INSERT
            LIMIT  1;
            """, (lng, lat, lng, lat))

        new_id = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()

        return {
            "message": "Successfully added blockage.",
            "lat": lat,
            "lng": lng,
            "id": new_id,
            "status": "SUCCESS",
        }


    # remove a blockage
    def delete(self):
        conn = get_db_connection()
        cur = conn.cursor()

        json_data = request.get_json(force=True)
        param_id = json_data['id']

        cur.execute("""
            DELETE FROM blockages
            WHERE id=%s
            """, [param_id])

        conn.commit()
        cur.close()
        conn.close()

        return {
            "message": "Successfully removed blockage.",
            "id": param_id,
            "status": "SUCCESS",
        }


class Routes(Resource):
    # get all routes given a source point and a destination point
    def get(self):
        args = request.args
        source_lat = float(args['source_lat'])
        source_lng = float(args['source_lng'])
        dest_lat = float(args['destination_lat'])
        dest_lng = float(args['destination_lng'])

        xmin = min(source_lng, dest_lng)
        xmax = max(source_lng, dest_lng)
        ymin = min(source_lat, dest_lat)
        ymax = max(source_lat, dest_lat)

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM   blockages
            WHERE  ST_GeomFromText(ST_AsText(geog)) @
                ST_MakeEnvelope (
                    %s, %s,     -- bounding 
                    %s, %s,     -- box limits
                    4326)       -- SRID for leaflet and OMS
        """, (str(xmin), str(ymin), str(xmax), str(ymax)))

        blockages = cur.fetchall()

        # convert to dict
        # make dict
        blockages_list = []
        for row in blockages:
            row_dict = {}
            row_dict["geog_wkb"] = row[1]

            # convert wkb to lat long
            point = wkb.loads(row[1])
            row_dict["lng"] = point.x
            row_dict["lat"] = point.y

            blockages_list.append(row_dict)

        cur.close()
        conn.close()

        paths = get_shortest_paths(blockages_list, source_lat, source_lng, dest_lat, dest_lng)

        return {
            "data": [path.to_json() for path in paths],
            "status": "SUCCESS",
        }


class Simulate(Resource):
    # get all routes given a source point and a destination point
    def get(self):
        args = request.args
        source_lat = args['source_lat']
        source_lng = args['source_lng']
        distance = args['distance']

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM   blockages
            WHERE  
                ST_DWithin(
                    geog, 
                    'POINT(%s %s)', 
                    %s
                )
        """ % (source_lng, source_lat, distance))

        blockages = cur.fetchall()

        # convert to dict
        # make dict
        blockages_list = []
        for row in blockages:
            row_dict = {}
            row_dict["geog_wkb"] = row[1]

            # convert wkb to lat long
            point = wkb.loads(row[1])
            row_dict["lng"] = point.x
            row_dict["lat"] = point.y

            blockages_list.append(row_dict)

        cur.close()
        conn.close()

        print(len(blockages_list))

        # we are making sure to pass the proper number types
        edge_list = run_simulation(blockages_list, float(source_lat), float(source_lng), int(float(distance)))

        routes_merged = gpd.GeoDataFrame( pd.concat( edge_list, ignore_index=True) )

        result = {
            "routes": routes_merged.to_json(),
        }

        return {
            "data": result,
            "status": "SUCCESS",
        }


api.add_resource(Home, "/")
api.add_resource(Blockages, "/blockages")
api.add_resource(Routes, "/routes")
api.add_resource(Simulate, "/simulate")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)