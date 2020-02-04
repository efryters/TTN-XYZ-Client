# Eric Fryters
# Flask app to serve database data and UI to browser

from flask import Flask, request, Response, render_template

from py_app_components import SQL_Database

import json

app = Flask(__name__, template_folder='./web/', static_folder="./web/")


@app.route('/')
@app.route('/index.html')
def index_html():
    return render_template("index.html")

@app.route('/get_data')
def get_from_sql():
    
    query_req = request.args.get('type')
    device_id = request.args.get('device_id')
    if query_req == "latest":
        data_req = {
            "type" : query_req,
            "device_id" : device_id
        }
    elif query_req == "ranged":
        time_from   = request.args.get('time_from')
        time_to     = request.args.get('time_to')
        data_req = {
            "type" : query_req,
            "from" : time_from,
            "to"   : time_to,
            "device_id" : device_id
        }
    else:
        return Response("Error")
        pass

    sql_db = SQL_Database("my_db.db")
    sql_db.open_database()
    data_return = sql_db.get_sensor_data(data_req)
    
    sql_db.close_database()

    
    return Response(json.dumps(data_return), content_type="application/json")
    
@app.route('/get_unique_devices')
def get_unique_devices():
    sql_db = SQL_Database("my_db.db")
    sql_db.open_database()
    data_return = sql_db.get_unique_devices()

    sql_db.close_database()

    return Response(json.dumps(data_return), content_type="application/json")

if __name__ == '__main__':
    
    app.run(host="0.0.0.0", port=8080)