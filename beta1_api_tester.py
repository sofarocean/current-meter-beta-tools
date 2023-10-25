# -------------------------------------------------------------------------------
# Name:        beta1_api_tester.py
# Purpose:     Tester for retrieving and decoding Current Meter data from the Sofar API
#
# Author:      evanShap
#
# Copyright:   (c) 2023 Sofar Ocean
# License:     Apache License, Version 2.0
# -------------------------------------------------------------------------------

import argparse
import json
from iso8601 import parse_date
from lib.api_functions import fetch_sensor_data
from lib.binary_decoder import decode_payload_to_structs, DVT1_DATA_CHANNELS, DVT1_STRUCT_DESCRIPTION

def convert_to_iso8601(date_str):
    try:
        parsed_date = parse_date(date_str)
        return parsed_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    except:
        raise ValueError("Invalid date/time format")

def main():
    parser = argparse.ArgumentParser(description='Retrieve and decode DVT1 data from the Sofar API.')
    parser.add_argument('spotter_id', type=str, help='Spotter ID')
    parser.add_argument('api_token', type=str, help='API Token')
    parser.add_argument('--start_date', type=convert_to_iso8601, help='Start date (optional)')
    parser.add_argument('--end_date', type=convert_to_iso8601, help='End date (optional)')

    args = parser.parse_args()

    try:
        api_response = fetch_sensor_data(args.spotter_id, args.api_token, args.start_date, args.end_date)
        for payload in api_response.get('data', []):
            hex_value = payload.get('value', '')
            timestamp = payload.get('timestamp', 'Unknown')
            try:
                decoded_value = decode_payload_to_structs(hex_value, DVT1_DATA_CHANNELS, DVT1_STRUCT_DESCRIPTION)
                payload['decoded_value'] = decoded_value
            except ValueError as ve:
                print(f"Failed to decode hex value {hex_value} at timestamp {timestamp}: {ve}")
                continue
        print(json.dumps(api_response, indent=4))
    except Exception as e:
        print(f"Failed to retrieve or decode data: {e}")


if __name__ == "__main__":
    main()
