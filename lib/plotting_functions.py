import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplcursors
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict

# Constants
DEFAULT_GAP_THRESHOLD = timedelta(minutes=65)
PLOT_WINDOW_HSIZE = 15
PLOT_WINDOW_VSIZE = 8


def extract_channel_data(data: dict, channel_name: str, gap_threshold_duration: timedelta = DEFAULT_GAP_THRESHOLD) -> tuple:
    """
    Extract channel specific data from input data.

    Parameters:
    - data (dict): The input data containing timestamps and channel values.
    - channel_name (str): The specific channel name to extract.
    - gap_threshold_duration (timedelta): Threshold to consider data as missing and introduce gaps.

    Returns:
    tuple: Containing lists for timestamps, mean_values, min_values, max_values, and std_values.
    """
    timestamps = []
    mean_values = []
    min_values = []
    max_values = []
    std_values = []
    last_timestamp = None

    for payload in data:
        timestamp = payload.get('timestamp', None)
        if timestamp:
            timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
        if last_timestamp and (timestamp - last_timestamp > gap_threshold_duration):
            timestamps.extend([last_timestamp, timestamp])
            mean_values.extend([np.nan, np.nan])
            min_values.extend([np.nan, np.nan])
            max_values.extend([np.nan, np.nan])
            std_values.extend([np.nan, np.nan])

        decoded_value = payload.get('decoded_value', [])
        channel_data = next((item for item in decoded_value if item['channel_name'] == channel_name), None)
        if channel_data:
            channel_stats = channel_data['data']
            timestamps.append(timestamp)
            mean_values.append(channel_stats['mean'])
            min_values.append(channel_stats['min'])
            max_values.append(channel_stats['max'])
            std_values.append(channel_stats['stdev'])

        last_timestamp = timestamp

    return timestamps, mean_values, min_values, max_values, std_values


def subplot_json_channel(ax, data: dict, channel_name: str, gap_threshold_duration: timedelta = DEFAULT_GAP_THRESHOLD) -> None:
    """
    Plot specific channel data on a given subplot.

    Parameters:
    - ax: The subplot axis to plot on.
    - data (dict): The input data.
    - channel_name (str): The specific channel name to plot.
    - gap_threshold_duration (timedelta): Threshold to consider data as missing and introduce gaps.
    """
    timestamps, mean_values, min_values, max_values, std_values = extract_channel_data(data, channel_name, gap_threshold_duration)
    ax.plot(timestamps, mean_values, linewidth=1.5, label='Mean', color='black', marker='o', markersize=3)
    ax.plot(timestamps, min_values, linewidth=1, label='Min', color='orange', marker='o', markersize=2)
    ax.plot(timestamps, max_values, linewidth=1, label='Max', color='purple', marker='o', markersize=2)
    fill_upper_bound = np.array(mean_values) + np.array(std_values)
    fill_lower_bound = np.array(mean_values) - np.array(std_values)
    ax.fill_between(timestamps, fill_lower_bound, fill_upper_bound, color='darkblue', alpha=0.2, label='Stdev')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M - %m/%d'))
    ax.set_xlabel('Timestamp')
    ax.set_ylabel(channel_name)
    ax.set_title(f'{channel_name} Over Time')
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    ax.grid(which='both', linestyle='--', linewidth=0.5, alpha=0.6)


def group_by_node_id(data: dict) -> defaultdict:
    """
    Group data by the bristlemouth_node_id.

    Parameters:
    - data (dict): The input data.

    Returns:
    defaultdict: Grouped data by node ID.
    """
    grouped_data = defaultdict(list)
    for payload in data.get('data', []):
        node_id = payload.get('bristlemouth_node_id', 'None')
        grouped_data[node_id].append(payload)
    return grouped_data


def plot_grouped_data(grouped_data: defaultdict, channel_names: list, gap_threshold_duration: timedelta = DEFAULT_GAP_THRESHOLD) -> None:
    """
    Plot data for each node ID.

    Parameters:
    - grouped_data (defaultdict): Data grouped by node ID.
    - channel_names (list): List of channel names to plot.
    - gap_threshold_duration (timedelta): Threshold to consider data as missing and introduce gaps.
    """
    for node_id, data_group in grouped_data.items():
        has_decoded_values = any([payload.get('decoded_value', []) for payload in data_group])

        if not has_decoded_values:
            continue

        fig, axes = plt.subplots(len(channel_names), 1, figsize=(PLOT_WINDOW_HSIZE, PLOT_WINDOW_VSIZE), sharex=True)

        if len(channel_names) == 1:
            axes = [axes]

        for i, channel_name in enumerate(channel_names):
            subplot_json_channel(axes[i], data_group, channel_name, gap_threshold_duration)

        fig.suptitle(f'Plots for node {node_id[:6]}', fontsize=16)
        mplcursors.cursor(hover=True)
        plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust for the suptitle
    # show all node plots
    plt.show()


def plot_json_channels(data: dict, channel_names: list, gap_threshold_duration: timedelta = DEFAULT_GAP_THRESHOLD) -> None:
    """
    Main function to plot JSON channel data.

    Parameters:
    - data (dict): The input data, formatted as sensor-data response json with decoded-values.
    -- see lib.api_functions.fetch_and_decode_sensor_data
    - channel_names (list): List of channel names to plot.
    -- see lib.binary_decoder.DVT1_DATA_CHANNELS
    - gap_threshold_duration (timedelta): Threshold to consider data as missing and introduce gaps.
    """
    grouped_data = group_by_node_id(data)
    plot_grouped_data(grouped_data, channel_names, gap_threshold_duration)

