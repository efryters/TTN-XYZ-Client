# TTN-XYZ-Client

## Description
This client is an example application for the data access of the sensor data. It connects to the TTN network via MQTT using the official TTN Python API. The data is collected to memory using a list and then those lists are used to populate charts for visual feedback of the sensor data. The Plotly Python API was used for the charting feature.

## Requirements
- Python 3.7 with Pip package manager
- Virtualenv

## Setup
1. Clone this repository
    ```bash
    user@host# git clone <url>
    ```
2. Change into directory of repository and create a Python3.7 environment using virtualenv
    ```bash
    user@host# virtualenv -p python3 env/
    ```

3. Activate the new environment and install the requirements
    ```bash
    user@host# source env/bin/activate
    (env) user@host# pip install -r requirements.txt
    ```

4. Edit client.py (if necessary) to set the device to be watched
    ```python
    device_id = "nucleo-all-sensors" # Change to appropriate device ID
    ```

5. Run the application
    ```bash
    (env) user@host# python client.py
    ```

## Running the application using client/server model.

1. Ensure that the environment in env/ is active, and pip installed requireed packages.
    ```bash
    user@host# source env/bin/activate
    (env) user@host# pip install -r requirements.txt
    ```

2. Modify mqtt_listener.py ttn_conn_info dict to point to the appropriate device to record. Edit the "device_id" field.
    ```python
        ttn_conn_info = {
            "app_id": "capstone-testing",
            "access_key": "#####################################",
            "device_id": "nucleo-all-sensors" #modify this to your device ID
        }
    ```

3. Run the mqtt application, and keep it running to collect data from TTN
    ```bash
    (env) user@host# python mqtt_listener.py
    ```

4. Next run the http application and keep it running. This will serve the HTML and javascript to view the data.
    ```bash
    (env) user@host# python http_listener.py
    ```

5. Navigate your browser to http://127.0.0.1:8080/ and follow the prompts.