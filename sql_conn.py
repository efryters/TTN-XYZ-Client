import sqlite3
from sqlite3 import Connection

import os.path
from os import path

import time

class SQL_Database:

    """
    Create a connection. Return True if successful
    """
    def __init__(self, db_file):
        self.db_file = db_file
        self.create_table_str = """ CREATE TABLE "ttn-data" (
                                    "ID"	        INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                                    "date"	        INTEGER,
                                    "device_id"	    TEXT,
                                    "light"	        REAL,
                                    "temperature"   REAL,
                                    "moisture"      REAL
                                )"""

    def open_database(self):

            # Check if db file exists, otherwise make a new one
            if path.exists(self.db_file):
                try:
                    self.connection = Connection(self.db_file)
                    print("[SQL] Connected to db " + self.db_file)
                    return True
                except Exception as e:

                    return e
            # Make a new db 
            else:
                try:
                    self.connection = Connection(self.db_file)
                    print("[SQL] Created db " + self.db_file)
                    self.make_table()

                except Exception as e:
                    return e

                pass


    def insert_sensor_data(self, obj):
        query = """ INSERT INTO "ttn-data" (date, device_id, light, temperature, moisture) VALUES (?, ?, ?, ?, ?) """

        data_out = [
            time.time(),
        ]

        data_out = (data_out + obj)
        with self.connection:
            c = self.connection.cursor()
            c.execute(query, data_out)
            print("[SQL] Inserted data at rowID: " + str(c.lastrowid))

        pass

    def get_data(self):

        pass


    def make_table(self):
        try:
            with self.connection:
                c = self.connection.cursor()
                c.execute(self.create_table_str)
                print("[SQL] Created tables for db")
            return True
        except Exception as e:
            return e
        
    def close_database(self):
        self.connection.close()
        print("[SQL] Closed database " + self.db_file)

    pass