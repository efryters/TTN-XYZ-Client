from py_app_components import TTN_MQTT_Client

def main():

    conn_data = {
        "device_id"     : "nucleo-all-sensors",
        "access_key"    : "ttn-account-v2.-iuXckSlRsK5ReT8eh2Np-34RVwoXMeMPNIDlr0jITM",
        "app_id"        : "capstone-testing"
    }

    ttn_client = TTN_MQTT_Client(conn_data)
    ttn_client.connect()

    #infinite loop
    while(True):
        # check if data exists
        while(not ttn_client.has_data()):
            pass
        # data exists
        print(ttn_client.get_data())


if __name__ == "__main__":
    main()