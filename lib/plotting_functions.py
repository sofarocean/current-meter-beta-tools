import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplcursors
import numpy as np
from datetime import datetime, timedelta

DEFAULT_GAP_THRESHOLD = timedelta(minutes=65)
PLOT_WINDOW_HSIZE = 15
PLOT_WINDOW_VSIZE = 8
def extract_channel_data(data, channel_name, gap_threshold_duration=DEFAULT_GAP_THRESHOLD):
    timestamps = []
    mean_values = []
    min_values = []
    max_values = []
    std_values = []
    last_timestamp = None

    for payload in data.get('data', []):
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


def subplot_json_channel(ax, data, channel_name, gap_threshold_duration=DEFAULT_GAP_THRESHOLD):
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


def plot_json_channels(data, channel_names, gap_threshold_duration=DEFAULT_GAP_THRESHOLD):
    n_channels = len(channel_names)
    fig, axes = plt.subplots(n_channels, 1, figsize=(PLOT_WINDOW_HSIZE, PLOT_WINDOW_VSIZE), sharex=True)
    if n_channels == 1:
        axes = [axes]
    for i, channel_name in enumerate(channel_names):
        subplot_json_channel(axes[i], data, channel_name, gap_threshold_duration)
    mplcursors.cursor(hover=True)
    plt.tight_layout(rect=[0, 0, 1, 1])
    plt.show()
