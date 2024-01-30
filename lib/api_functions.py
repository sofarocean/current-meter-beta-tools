# -------------------------------------------------------------------------------
# Name:        api_functions.py
# Purpose:     Fetch sensor-data from Sofar API
#
# Author:      evanShap
#
# Copyright:   (c) 2023 Sofar Ocean
# License:     Apache License, Version 2.0
# -------------------------------------------------------------------------------

import json
import re
import requests

from lib.beta2_data import group_sensor_data, format_data_for_plotting
from lib.binary_decoder import decode_payload_to_structs, DVT1_DATA_CHANNELS, DVT1_STRUCT_DESCRIPTION


def validate_iso_8601_timestamp(timestamp):
    """Validate if a given string is a valid ISO-8601 timestamp."""
    pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'
    return re.match(pattern, timestamp) is not None


def fetch_sensor_data(spotter_id, api_token, start_date=None, end_date=None):
    """Fetch sensor-data from Sofar API."""

    if start_date and not validate_iso_8601_timestamp(start_date):
        raise ValueError("Invalid start_date format. Must be ISO-8601.")
    if end_date and not validate_iso_8601_timestamp(end_date):
        raise ValueError("Invalid end_date format. Must be ISO-8601.")

    base_url = "https://api.sofarocean.com/api/sensor-data"
    params = {
        "token": api_token,
        "spotterId": spotter_id
    }
    if start_date:
        params["startDate"] = start_date
    if end_date:
        params["endDate"] = end_date

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise Exception(f"API request failed: {e}")


def fetch_and_decode_sensor_data(spotter_id, api_token, start_date=None, end_date=None):
    api_response = fetch_sensor_data(spotter_id, api_token, start_date, end_date)
    for payload in api_response.get('data', []):
        hex_value = payload.get('value', '')
        timestamp = payload.get('timestamp', 'Unknown')
        try:
            assert payload.get('units', None) == "hex"
            decoded_value = decode_payload_to_structs(hex_value, DVT1_DATA_CHANNELS, DVT1_STRUCT_DESCRIPTION)
            payload['decoded_value'] = decoded_value
        except AssertionError as e:
            print(f"Unexpected units type '{payload.get('units', None)}' for payload at time {payload.get('timestamp', 'Unknown')} is not type 'hex'. Skipping decoding.")
            continue
        except ValueError as ve:
            print(f"Failed to decode hex value {hex_value} at timestamp {timestamp}: {ve}")
            continue
    return api_response

def fetch_and_decode_beta2_data(spotter_id, api_token, start_date=None, end_date=None):
    api_response = fetch_sensor_data(spotter_id, api_token, start_date, end_date)
    grouped_location_data = group_sensor_data(api_response['data'])
    formatted_data = format_data_for_plotting(grouped_location_data)
    return {
        "data": formatted_data
    }

if __name__ == "__main__":
    # Sample usage
    api_token = input("Please paste your API token: ")
    spotter_id = input("Please paste your Spotter ID: ")

    sensor_data = fetch_sensor_data(spotter_id, api_token)
    print(json.dumps(sensor_data, indent=4))