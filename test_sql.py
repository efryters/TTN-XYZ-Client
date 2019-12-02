from py_app_components import SQL_Database
import time

def main():

    minutes_back = 30

    """ Packet data in structure """
    data_in = [
        "some-device",      # Device name
        124.2,              # Lux
        26.5,               # Temperaure (celcius)
        3355                # Moisture raw value
    ]

    time_from = time.time() - (60 * minutes_back)
    time_to   = time.time()

    db = SQL_Database("my_db.db")
    ret = db.open_database()

    db.insert_sensor_data(data_in)

    data_req_latest = {
        "type" : "latest"
    }

    data_req_ranged = {
        "type" : "ranged",
        "from" : time_from,
        "to"   : time_to
    }

    rows    = db.get_sensor_data(data_req_latest)
    rows_2  = db.get_sensor_data(data_req_ranged)

    db.close_database()




if __name__ == "__main__":
    main()