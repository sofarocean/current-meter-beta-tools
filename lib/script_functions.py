# -------------------------------------------------------------------------------
# Name:        script_functions.py
# Purpose:     Functions for processing channel data and generating handles.
#
# Author:      evanShap
#
# Copyright:   (c) 2023 Sofar Ocean
# License:     Apache License, Version 2.0
# -------------------------------------------------------------------------------

import re
from lib.binary_decoder import DVT1_DATA_CHANNELS
import argparse


def get_plot_handles_for_channels(channels):
    """
    Given a list of channels, returns a list where each element is a list of size two.
    The first element is the 'handle' derived from the channel name and the second is the original channel name.

    Args:
        channels (list): List of channel names.

    Returns:
        list: List of [handle, original channel name].
    """

    handles = []
    for channel in channels:
        # Convert to lowercase, remove spaces and units (e.g., [cm/s])
        handle = re.sub(r'\[.*\]', '', channel).replace(' ', '').lower()
        handles.append([handle, channel])

    return handles


def add_plot_arg_from_handles(parser, handle_list):
    """
    Add an argparse argument to the provided parser for specifying channels to plot.

    Parameters:
    - parser: argparse.ArgumentParser
        The argument parser to which the argument should be added.
    - handle_list: list of tuples
        A list of tuples where the first element is the handle and the second is the full name.

    The argument will be called '--plot-channels' with a short form '-pc' and will allow
    the user to specify a list of channels by their handle. An additional choice of 'all'
    is also available to specify all channels.
    """

    handles = [entry[0] for entry in handle_list]
    valid_choices = handles + ['all']

    help_string = "Specify the list of channels to plot. Set to 'all' to plot all available channels. "\
                  "To specify multiple channels, separate them with a space. "\
                  "Example: -pc handle1 handle2\nOptions:\n"
    for handle, full_name in handle_list:
        help_string += f"{handle}: {full_name}\n"

    parser.add_argument("-pc", "--plot_channels",
                        choices=valid_choices,
                        nargs='*',
                        help=help_string)


def get_channels_from_args(args, full_plot_handles):
    """
    Return the list of original channel names based on selected plot handles.

    Parameters:
    - args: Argument list, typically parsed from command-line input
    - full_plot_handles: List of pairs containing (handle, original channel name).
        See get_plot_handles_for_channels

    Returns:
    List of selected original channel names
    """

    if args is None:
        return []

    if 'all' in args:
        return [channel[1] for channel in full_plot_handles]

    selected_channels = []
    for handle, channel_name in full_plot_handles:
        if handle in args:
            selected_channels.append(channel_name)

    return selected_channels


# Test
if __name__ == "__main__":
    print(get_plot_handles_for_channels(DVT1_DATA_CHANNELS))
