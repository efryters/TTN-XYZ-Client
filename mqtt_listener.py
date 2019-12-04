# This application listens for MQTT messages and decodes/inserts to SQL database

from py_app_components import TTN_MQTT_Client
from py_app_components import SQL_Database
from py_app_components import Payload_Decoder

# Access info
ttn_conn_info = {
    "app_id": "capstone-testing",
    "access_key": "ttn-account-v2.-iuXckSlRsK5ReT8eh2Np-34RVwoXMeMPNIDlr0jITM",
    "device_id": "nucleo-all-sensors"
}

# Moisture calibration info
moisture_cal_air = 3550;
moisture_cal_water = 1750;

def main():
    # setup ttn connection
    ttn_client = TTN_MQTT_Client(ttn_conn_info)
    ttn_client.connect()

    # Setup the sql connection
    sql_db = SQL_Database("my_db.db")

    # create the payload decoder and input moisture calibraation data
    payload_decoder = Payload_Decoder()
    payload_decoder.set_moisture_calibration(moisture_cal_air, moisture_cal_water)

    # keep app running, update chart as data comes in
    while True:

        while(not ttn_client.has_data()):
            pass

        # check queue for raw data and process if there is
            raw_str = ttn_client.get_data().payload_raw
            if isinstance(raw_str, NotImplementedError):
                pass
            else:
                # Send data to the client
                [temperature_raw, moisture_raw, light_raw] = payload_decoder.decode_payload(
                    raw_str, return_single=True)

                data_to_db = [
                    ttn_conn_info["device_id"],
                    float(light_raw),
                    float(temperature_raw),
                    moisture_raw
                ]
                
                # Insert the data to SQL table
                if sql_db.open_database(): 
                    sql_db.insert_sensor_data(data_to_db)
                    sql_db.close_database()
                else:
                    print("[TTN-MQTT] Error sending to database.")



if __name__ == "__main__":
    main()
