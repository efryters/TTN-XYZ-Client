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
    user@host# pip install -r requirements.txt
    ```

4. Edit client.py (if necessary) to set the device to be watched
    ```python
    device_id = "nucleo-all-sensors" # Change to appropriate device ID
    ```

5. Run the application
    ```bash
    user@host# python client.py
    ```

## Running the application after setup procedure

1. Ensure that the environment in env/ is active
    ```bash
    user@host# source env/bin/activate
    ```

2. Run the application
    ```bash
    user@host# python client.py
    ```