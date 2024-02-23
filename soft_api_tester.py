# -------------------------------------------------------------------------------
# Name:        soft_api_tester.py
# Purpose:     Tester for retrieving and decoding Feb '24 DVT SOFT data from the Sofar API
#
# Author:      towynlin
#
# Copyright:   (c) 2024 Sofar Ocean
# License:     Apache License, Version 2.0
# -------------------------------------------------------------------------------

import argparse
from iso8601 import parse_date
from lib.api_functions import fetch_and_decode_soft_data
from lib.plotting_functions import plot_beta2_json_channels
from lib.script_functions import (
    get_plot_handles_for_channels,
    add_plot_arg_from_handles,
    get_channels_from_args,
)
import logging

# Configure logging (this is a basic configuration, adjust as needed)
logging.basicConfig(level=logging.INFO)

SOFT_DATA_CHANNELS = [
    "Temperature[ºC]",
]

soft_plot_handles = get_plot_handles_for_channels(SOFT_DATA_CHANNELS)


def convert_to_iso8601(date_str):
    try:
        parsed_date = parse_date(date_str)
        return parsed_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        raise ValueError("Invalid date/time format")


def main():
    parser = argparse.ArgumentParser(
        description="Retrieve and decode SOFT data from the Sofar API."
    )
    parser.add_argument("spotter_id", type=str, help="Spotter ID")
    parser.add_argument("api_token", type=str, help="API Token")
    parser.add_argument(
        "-s", "--start_date", type=convert_to_iso8601, help="Start date (optional)"
    )
    parser.add_argument(
        "-e", "--end_date", type=convert_to_iso8601, help="End date (optional)"
    )
    add_plot_arg_from_handles(parser, soft_plot_handles)
    args = parser.parse_args()
    channels_to_plot = get_channels_from_args(args.plot_channels, soft_plot_handles)
    print(channels_to_plot)
    try:
        print(f"Fetching SOFT data from sensor-data API...")
        decoded_api_response = fetch_and_decode_soft_data(
            args.spotter_id, args.api_token, args.start_date, args.end_date
        )
        print(f"Retrieved {len(decoded_api_response['data'])} samples.")
        print(f"Plotting channels {channels_to_plot}")
        plot_beta2_json_channels(decoded_api_response, channels_to_plot)

    except Exception as e:
        logging.error(f"Failed to retrieve or decode data: {e}", exc_info=True)


if __name__ == "__main__":
    main()
