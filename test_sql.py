from sql_conn import SQL_Database
import time

def main():

    data_in = [
        "some-device",
        124.2,
        26.5,
        3355
    ]

    db = SQL_Database("my_db.db")
    ret = db.open_database()

    db.insert_sensor_data(data_in)


    db.close_database()

    pass



if __name__ == "__main__":
    main()