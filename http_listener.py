# Serves database data to browser

from flask import Flask, request, Response

from py_app_components import SQL_Database

import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/get_data')
def get_from_sql():
    
    query_req = request.args.get('type')
    if query_req == "latest":
        data_req = {
            "type" : query_req
        }
        pass
    elif query_req == "ranged":
        time_from   = request.args.get('time_from')
        time_to     = request.args.get('time_to')
        data_req = {
            "type" : query_req,
            "from" : time_from,
            "to"   : time_to
        }
        pass
    else:
        return Response("Error")
        pass

    sql_db = SQL_Database("my_db.db")
    sql_db.open_database()
    data_return = sql_db.get_sensor_data(data_req)
    
    sql_db.close_database()

    
    return Response(json.dumps(data_return), content_type="application/json")
    

if __name__ == '__main__':
    app.run()