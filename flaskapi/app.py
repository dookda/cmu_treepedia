from auth import conn
import json
import os
from flask import Flask, redirect, url_for, request, jsonify
from flask_cors import CORS, cross_origin
import psycopg2 as pg2

app = Flask(__name__)
CORS(app, support_credentials=True)

host = conn["dbHost"]
db = conn["dbName"]
username = conn["dbUser"]
password = conn["dbPass"]
port = conn["dbPort"]
pg = pg2.connect(database=db, user=username,
                 password=password, host=host, port=port)

pg.autocommit = True
cur = pg.cursor()
print(cur)


@app.route('/hello')
@cross_origin()
def hello():
    return json.dumps({'msg': 'hello da'})


@app.route('/getpixelvalue/<string:index>/<string:yyyymmdd>/<float:latitude>/<float:longitude>')
@cross_origin()
def getPixelValue(index, yyyymmdd, latitude, longitude):
    f = f'./{index}_clip/_{yyyymmdd}_500m_32647_{index}_clip.tif'
    res = os.popen(
        f'gdallocationinfo -valonly -wgs84 {f} {longitude} {latitude}').read()

    return json.dumps({'index': index, 'val': res})


@app.route('/get_data')
@cross_origin()
def get_data():
    try:
        print("da")
        cur.execute('''SELECT * from base_sta''')
        rows = cur.fetchall()
        return jsonify(rows), 200
    except Exception as e:
        print(e)
        return []


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3100, debug=True)
