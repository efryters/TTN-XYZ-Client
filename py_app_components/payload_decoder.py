"""
payload_decoder.py
"""

import base64
import math
from decimal import Decimal, ROUND_DOWN
from datetime import date, datetime

class Payload_Decoder():

    def __init__(self):
        self.temperature_raw        = []
        self.moisture_raw           = []
        self.light_raw              = []

    def set_moisture_calibration(self, cal_air, cal_water):
        self.moisture_cal_air       = cal_air
        self.moisture_cal_water     = cal_water

    def decode_payload(self, bytes_in):
        raw_bytes       = base64.decodebytes(bytes_in.encode())
        exponent        = raw_bytes[1];
        mantissa        = raw_bytes[2];
        lux             = math.pow(2, exponent) * mantissa * 0.045;

        rawTemp         = (raw_bytes[3] << 8) | (raw_bytes[4]);
        procTemp        = (rawTemp / 100) - 55;
        procTemp_fixed  = Decimal(procTemp).quantize(Decimal('.01'), ROUND_DOWN)
        lux_fixed       = Decimal(lux).quantize(Decimal('.01'), ROUND_DOWN)
        moisture        = (raw_bytes[5] << 8) | (raw_bytes[6]);

        self.light_raw.append(lux_fixed)
        self.moisture_raw.append(moisture)
        self.temperature_raw.append(procTemp_fixed)

        # shift data as per decoder on TTN
        dt = datetime.today()
        print("[" + dt.strftime("%D %H:%M:%S") + "] MSG-UPLINK: Temperature: " + procTemp_fixed.to_eng_string() + "; Moisture: " + self.moisture_fuzzy_out(moisture) + "; Lux: " + lux_fixed.to_eng_string())
        print("Raw Moisture: " + str((moisture)))
        return [ self.temperature_raw, self.moisture_raw, self.light_raw ]

    def moisture_fuzzy_out(self, moisture_in):
        moisture_sections = (self.moisture_cal_air - self.moisture_cal_water) / 3
        if moisture_in > self.moisture_cal_water and moisture_in < (self.moisture_cal_water + moisture_sections):
            return "Saturated"
        elif moisture_in > (self.moisture_cal_water + moisture_sections) and moisture_in < (self.moisture_cal_air - moisture_sections):
            return "Wet"
        elif moisture_in < self.moisture_cal_air and moisture_in > (self.moisture_cal_air - moisture_sections):
            return "Dry"
        else:
            return "Error"