# -------------------------------------------------------------------------------
# Name:        api_functions.py
# Purpose:     Fetch sensor-data from Sofar API
#
# Author:      evanShap
#
# Copyright:   (c) 2023 Sofar Ocean
# License:     Apache License, Version 2.0
# -------------------------------------------------------------------------------

import requests
import json
import re


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


if __name__ == "__main__":
    # Sample usage
    api_token = input("Please paste your API token: ")
    spotter_id = input("Please paste your Spotter ID: ")

    sensor_data = fetch_sensor_data(spotter_id, api_token)
    print(json.dumps(sensor_data, indent=4))