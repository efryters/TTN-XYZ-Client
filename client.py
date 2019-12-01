# Eric Fryters
# App to receive data from TTN API
# and plot to graphs for Thursday demo

import time
from datetime import date, datetime
import signal
import math
from decimal import Decimal, ROUND_DOWN
import queue
import ttn
import base64

from plotly.subplots import make_subplots
import plotly.graph_objects as go

from sql_conn import SQL_Database

# Access info
app_id = "capstone-testing"
access_key = "ttn-account-v2.-iuXckSlRsK5ReT8eh2Np-34RVwoXMeMPNIDlr0jITM"
device_id = "nucleo-all-sensors"

# Moisture calibration info
moisture_cal_air = 3550;
moisture_cal_water = 1750;

# Data
temperature_raw = []
moisture_raw = []
light_raw = []
msg_queue = queue.Queue()

def moisture_fuzzy_out(moisture_in):
  moisture_sections = (moisture_cal_air - moisture_cal_water) / 3
  if moisture_in > moisture_cal_water and moisture_in < (moisture_cal_water + moisture_sections):
    return "Saturated"
  elif moisture_in > (moisture_cal_water + moisture_sections) and moisture_in < (moisture_cal_air - moisture_sections):
    return "Wet"
  elif moisture_in < moisture_cal_air and moisture_in > (moisture_cal_air - moisture_sections):
    return "Dry"
  else:
    return "Error"

def decode_payload(bytes_in):
  raw_bytes = base64.decodebytes(bytes_in.encode())
  exponent = raw_bytes[1];
  mantissa = raw_bytes[2];
  lux = math.pow(2, exponent) * mantissa * 0.045;

  rawTemp = (raw_bytes[3] << 8) | (raw_bytes[4]);
  procTemp = (rawTemp / 100) - 55;
  procTemp_fixed = Decimal(procTemp).quantize(Decimal('.01'), ROUND_DOWN)
  lux_fixed = Decimal(lux).quantize(Decimal('.01'), ROUND_DOWN)
  moisture = (raw_bytes[5] << 8) | (raw_bytes[6]);

  light_raw.append(lux_fixed)
  moisture_raw.append(moisture)
  temperature_raw.append(procTemp_fixed)

  # shift data as per decoder on TTN
  dt = datetime.today()
  print("[" + dt.strftime("%D %H:%M:%S") + "] MSG-UPLINK: Temperature: " + procTemp_fixed.to_eng_string() + "; Moisture: " + moisture_fuzzy_out(moisture) + "; Lux: " + lux_fixed.to_eng_string())
  print("Raw Moisture: " + str((moisture)))

def uplink_callback(msg, client):
  #print("Received uplink from ", msg.dev_id)
  #print(msg)
  if msg.dev_id == device_id:
    msg_queue.put(msg.payload_raw)
  else:
    msg_queue.put(NotImplementedError("Device ID non-existant"))
 
def connect_callback(res, client):
  if res:
    print("Connected to TTN.")
  else:
    print("Connection problem with TTN.")


"""
Entry-point for application
"""
def main():
  # setup ttn connection
  handler = ttn.HandlerClient(app_id, access_key)
  mqtt_client = handler.data()
  mqtt_client.set_uplink_callback(uplink_callback)
  mqtt_client.set_connect_callback(connect_callback)
  mqtt_client.connect()


  # keep app running, update chart as data comes in
  while True:
    # check queue for raw data and process if there is
    if not msg_queue.qsize() == 0:
      raw_str = msg_queue.get()
      
      if isinstance(raw_str, NotImplementedError):
        pass
      else:
        decode_payload(raw_str)
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

        fig.write_html('chart.html', auto_open=False)
        #raise raw_str
      



    pass
  #mqtt_client.close()

if __name__ == '__main__':
  main()
