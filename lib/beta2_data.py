# -------------------------------------------------------------------------------
# Name:        beta2_data.py
# Purpose:     Manipulate Beta 2 sensor-data from Sofar API
#
# Author:      evanShap
#
# Copyright:   (c) 2024 Sofar Ocean
# License:     Apache License, Version 2.0
# -------------------------------------------------------------------------------

from itertools import groupby
import logging
from math import degrees
from operator import itemgetter

# Configure logging (this is a basic configuration, adjust as needed)
logging.basicConfig(level=logging.INFO)

def group_sensor_data(data):
    """
       Group Beta 2 sensor-data response by location datum (latitude, longitude, timestamp, and sensorPosition).

       Parameters:
       data (list of dict): A list of dictionaries where each dictionary represents
                            sensor data with keys like latitude, longitude, timestamp,
                            sensorPosition, units, value, unit_type, and data_type_name.
                            See docs/example_beta2_sensor-data_payload.json for expected input structure.

       Returns:
       list of dict: A list of dictionaries, each containing the keys 'latitude',
                     'longitude', 'timestamp', 'sensorPosition' and a 'sample_values' list
                     with the grouped sensor data.
       """
    # Modify each dictionary to ensure 'bristlemouth_node_id' key exists with a default value of None
    for entry in data:
        entry.setdefault('bristlemouth_node_id', None)

    # Sort the data by the keys you want to group by
    data.sort(key=itemgetter('timestamp', 'latitude', 'longitude', 'sensorPosition'))

    # Use groupby to group data
    grouped_data = [
        {
            "timestamp": timestamp,
            "latitude": latitude,
            "longitude": longitude,
            "sensorPosition": sensorPosition,
            "bristlemouth_node_id": bristlemouth_node_id,
            "sample_values": [
                {
                    "units": item["units"],
                    "value": item["value"],
                    "unit_type": item["unit_type"],
                    "data_type_name": item["data_type_name"]
                }
                for item in items
            ]
        }
        for (timestamp, latitude, longitude, sensorPosition, bristlemouth_node_id), items in
        groupby(data, key=itemgetter('timestamp', 'latitude', 'longitude', 'sensorPosition', 'bristlemouth_node_id'))
    ]

    return grouped_data

def format_data_for_plotting(data):
    """
    Format sensor data for plotting purposes.

    This function iterates through a list of sensor data, each represented as a dictionary,
    and formats it into a more structured format suitable for plotting. It organizes
    various measurements into a new list under the 'decoded_value' key within each datum.

    Parameters:
    data (list of dict): output of group_sensor_data

    Returns:
    list of dict: The input list with modified dictionaries containing 'decoded_value'
                  key with formatted data for plotting.
    """
    for located_datum in data:
        try:
            sample_values_dict = {}
            for sample_value in located_datum['sample_values']:
                sample_values_dict[sample_value['data_type_name']] = sample_value

            if (
                "aanderaa_abs_speed_mean_15bits" not in sample_values_dict
                and "aanderaa_abs_tilt_mean_8bits" in sample_values_dict
                and degrees(sample_values_dict["aanderaa_abs_tilt_mean_8bits"]["value"])
                > 75.0
            ):
                print(f"Sensor {located_datum['sensorPosition']} horizontal at {located_datum['timestamp']}")
                continue
            elif "aanderaa_abs_tilt_mean_8bits" not in sample_values_dict:
                position, timestamp = located_datum["sensorPosition"], located_datum["timestamp"]
                print(f"Sensor {position} has no tilt data at {timestamp}")
                continue

            located_datum['decoded_value'] = [
                 {
                    "data": {
                        "sample_count": sample_values_dict['aanderaa_reading_count_10bits']['value'],
                        "mean": sample_values_dict['aanderaa_abs_speed_mean_15bits']['value'],
                        "stdev": sample_values_dict['aanderaa_abs_speed_std_15bits']['value']
                    },
                    "channel_name": "Abs Speed[cm/s]"
                },
                {
                    "data": {
                        "sample_count": sample_values_dict['aanderaa_reading_count_10bits']['value'],
                        "mean": degrees(sample_values_dict['aanderaa_abs_tilt_mean_8bits']['value']),
                        "stdev": degrees(sample_values_dict['aanderaa_std_tilt_mean_8bits']['value'])
                    },
                    "channel_name": "Abs Tilt[Deg]"
                },
                {
                    "data": {
                        "sample_count": sample_values_dict['aanderaa_reading_count_10bits']['value'],
                        "mean": degrees(sample_values_dict['aanderaa_direction_circ_mean_13bits']['value']),
                        "stdev": degrees(sample_values_dict['aanderaa_direction_circ_std_13bits']['value'])
                    },
                    "channel_name": "Direction[Deg.M]"
                },
                {
                    "data": {
                        "sample_count": sample_values_dict['aanderaa_reading_count_10bits']['value'],
                        "mean": sample_values_dict['aanderaa_temperature_mean_13bits']['value']
                    },
                    "channel_name": "Temperature[ºC]"
                }
            ]
        except Exception as e:
            print(f"Could not format data for sensor {located_datum['sensorPosition']}, at {located_datum['timestamp']}")
            logging.error(f"Error: {e}", exc_info = True)
            continue
    return data

def format_soft_data_for_plotting(data):
    """Format SOFT module data for plotting purposes."""
    for located_datum in data:
        try:
            sample_values_dict = {}
            for sample_value in located_datum["sample_values"]:
                sample_values_dict[sample_value["data_type_name"]] = sample_value

            if "bm_soft_temperature_mean_13bits" not in sample_values_dict:
                continue

            located_datum["decoded_value"] = [
                {
                    "data": {
                        "mean": sample_values_dict["bm_soft_temperature_mean_13bits"][
                            "value"
                        ],
                    },
                    "channel_name": "Temperature[ºC]",
                }
            ]
        except Exception as e:
            print(
                f"Could not format data for sensor {located_datum['sensorPosition']}, at {located_datum['timestamp']}"
            )
            logging.error(f"Error: {e}", exc_info=True)
            continue
    return data
