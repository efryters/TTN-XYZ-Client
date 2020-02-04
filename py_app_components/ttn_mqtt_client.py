import ttn
import queue

class TTN_MQTT_Client():

    def __init__(self, conn_obj):

        self.app_id =  conn_obj["app_id"]
        self.access_key = conn_obj["access_key"]
        self.device_id = conn_obj["device_id"]
        self.msg_queue = queue.Queue()

        self.handler = ttn.HandlerClient(self.app_id, self.access_key)
        self.mqtt_client = self.handler.data()
        self.mqtt_client.set_uplink_callback(self.__uplink_callback)
        self.mqtt_client.set_connect_callback(self.__connect_callback)

    def __uplink_callback(self, msg, client):
        #if msg.dev_id == self.device_id:
        self.msg_queue.put(msg)
        #else:
        #    self.msg_queue.put(NotImplementedError("Device ID non-existant"))

    def __connect_callback(self, res, client):
        if res:
            print("[TTN-MQTT] Connected to TTN")
        else:
            print("[TTN-MQTT] Connection to TTN not successful")

    def connect(self):
        self.mqtt_client.connect()

    def has_data(self):
        if self.msg_queue.qsize() == 0:
            #print("No data in queue")
            return False
        else:
            #print("Data in queue")
            return True

    def get_data(self):
        payload = self.msg_queue.get()
        return payload

