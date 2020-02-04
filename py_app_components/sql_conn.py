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
        self.tables = ["ttn-devices", "ttn-data"]


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
                    return True

                except Exception as e:
                    return e


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

    def get_sensor_data(self, get_type):
        query = """ SELECT date, device_id, light, temperature, moisture FROM "ttn-data"
                    WHERE date >= ?
                    AND   date <= ?
                    AND   device_id = ?
                """

        if get_type["type"] == "latest":
            query_params = [
                time.time() - (30 * 60),
                time.time(),
                get_type["device_id"]
            ]
            msg_type = "[SQL] Query type: Latest data of past 30 minutes."
            
        elif get_type["type"] == "ranged":
            query_params = [
                get_type["from"],
                get_type["to"],
                get_type["device_id"]
            ]
            msg_type = "[SQL] Query type: Ranged data provided by query."
        else:
            msg_type = "[SQL] Query type blank, no query executed."
            return []
        with self.connection:
            c = self.connection.cursor()
            c.execute(query, query_params)

            rows_returned = c.fetchall()

            print(msg_type)
            print("[SQL] Returned " + str(len(rows_returned)) + " rows.")

            return rows_returned


    def make_table(self):
        create_table_str = """ CREATE TABLE "ttn-data" (
                            "ID"	        INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                            "date"	        INTEGER,
                            "device_id"	    TEXT,
                            "light"	        REAL,
                            "temperature"   REAL,
                            "moisture"      REAL
                        )"""
        try:
            with self.connection:
                c = self.connection.cursor()
                c.execute(create_table_str)
                print("[SQL] Created tables for db")
            return True
        except Exception as e:
            return e
        
    def make_table_devices(self):
        create_table_str = """ CREATE TABLE "ttn-devices" (
                            "id"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                            "device-friendly-name"	TEXT,
                            "device-eui"	TEXT
                            )"""
        try:
            with self.connection:
                c = self.connection.cursor()
                c.execute(create_table_str)
                print("[SQL] Created tables for db")
            return True
        except Exception as e:
            return e
                        

    def close_database(self):
        self.connection.close()
        print("[SQL] Closed database " + self.db_file)

    def check_table_exist(self, table):

        query_str = """ SELECT count(name) FROM sqlite_master WHERE type="table" AND name=""" + str(table) + """" """
        with self.connection:
            c = self.connection.cursor()
            c.execute(query_str)

            if c.fetchone()[0] == 1:
                print("Table exists")
                return True
            else:
                print("Table not exist")
                return False 

    def get_unique_devices(self):

        query_str = """ SELECT DISTINCT "device_id" from "ttn-data" """
        msg_type = "[SQL] Fetching unique device names"

        with self.connection:
            c = self.connection.cursor()
            c.execute(query_str)

            rows_returned = c.fetchall()

            print(msg_type)
            print("[SQL] Returned " + str(len(rows_returned)) + " rows.")

            return rows_returned


        pass