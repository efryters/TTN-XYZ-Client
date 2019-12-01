# Eric Fryters
# App to receive data from TTN API
# and plot to graphs for Thursday demo

import time
from datetime import date, datetime
import signal
import math
from decimal import Decimal, ROUND_DOWN
import queue
import base64

from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Custom libraries
from sql_conn import SQL_Database
from ttn_mqtt_client import TTN_MQTT_Client
from payload_decoder import Payload_Decoder

# Access info
ttn_conn_info = {
  "app_id" : "capstone-testing",
  "access_key" : "ttn-account-v2.-iuXckSlRsK5ReT8eh2Np-34RVwoXMeMPNIDlr0jITM",
  "device_id" : "nucleo-all-sensors"
}

# Moisture calibration info
moisture_cal_air = 3550;
moisture_cal_water = 1750;


"""
Entry-point for application
"""
def main():

  # setup ttn connection
  ttn_client = TTN_MQTT_Client(ttn_conn_info)
  ttn_client.connect()

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
        [ temperature_raw, moisture_raw, light_raw ] = payload_decoder.decode_payload(raw_str)
        # build the plots
        fig = make_subplots(
          rows=3, cols=1,
          subplot_titles=("Temperature", "Moisture", "Light")
          )

        # temperature
        fig.append_trace(
          go.Scatter(y=temperature_raw),
          row=1, col=1
        )
        # moisture
        fig.append_trace(
          go.Scatter(y=moisture_raw),
          row=2, col=1
        )
        # lux
        fig.append_trace(
          go.Scatter(y=light_raw),
          row=3, col=1
        )

        #fig = go.Figure(data=go.Line(y=temperature_raw))
        fig.update_layout(
          title_text="Sensor readings"
        )

        # update each plot axis
        # Update xaxis properties
        fig.update_xaxes(title_text="Time", row=1, col=1) # Tempeature
        fig.update_xaxes(title_text="Time", row=2, col=1) # Moisture
        fig.update_xaxes(title_text="Time", row=3, col=1) # Light

        # Update yaxis properties
        fig.update_yaxes(title_text="Temperature (C)", row=1, col=1)
        fig.update_yaxes(title_text="Moisture (raw)", row=2, col=1)
        fig.update_yaxes(title_text="Light Sense (lux)", row=3, col=1)

        fig.write_html('chart_2.html', auto_open=False)
        #raise raw_str
    pass
  #mqtt_client.close()

if __name__ == '__main__':
  main()
