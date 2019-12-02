# Serves database data to browser

from flask import Flask

from py_app_components import SQL_Database

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/get_data', method=['GET'])
def get_from_sql():
    sql_db = SQL_Database("my_db.db")
    sql_db.open_database()

    

if __name__ == '__main__':
    app.run()