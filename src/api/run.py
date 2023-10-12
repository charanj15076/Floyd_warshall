import os
import psycopg2
import json
import datetime
from shapely import wkb

from dotenv import load_dotenv

import flask
from flask import request
from flask_restful import Resource, Api
from flask_cors import CORS

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
            INSERT INTO blockages (geog)
                VALUES ('POINT(%s %s)')
            RETURNING id;
            """, (lng, lat))

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
            "message": "Successfully added blockage.",
            "id": param_id,
            "status": "SUCCESS",
        }


api.add_resource(Home, "/")
api.add_resource(Blockages, "/blockages")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)