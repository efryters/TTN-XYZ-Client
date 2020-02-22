# This application listens for MQTT messages and decodes/inserts to SQL database

from py_app_components import TTN_MQTT_Client
from py_app_components import SQL_Database
from py_app_components import Payload_Decoder
import time

# Access info
ttn_conn_info = {
    "app_id": "capstone-testing",
    "access_key": "ttn-account-v2.d-twriMNDaeMQtzMyr1afJfOCynrwHtQoHDKRJ1khKU",
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
            time.sleep(0.1)    
            pass

        # check queue for raw data and process if there is
            
        raw_msg = ttn_client.get_data()
        if isinstance(raw_msg, NotImplementedError):
            print("[TTN-MQTT] Received other device data. Ignored.")
            pass
        else:
            try:
                raw_str = raw_msg.payload_raw
            # Send data to the client
                [temperature_raw, moisture_raw, light_raw] = payload_decoder.decode_payload(
                    raw_str, return_single=True)


                data_to_db = [
                    raw_msg.dev_id,
                    float(light_raw),
                    float(temperature_raw),
                    moisture_raw
                ]

                # Insert the data to SQL table
                if sql_db.open_database(): 
                    sql_db.insert_sensor_data(data_to_db)
                    sql_db.close_database()
                    print("[TTN-MQTT] Sent device " + raw_msg.dev_id + " to database.")
                else:
                    print("[TTN-MQTT] Error sending to database.")
            except Exception as e:
                print("[TTN-MQTT] Error: invalid data in.")
                data_to_db = []
                               

if __name__ == "__main__":
    main()
