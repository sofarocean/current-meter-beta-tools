# -------------------------------------------------------------------------------
# Name:        binary_decoder.py
# Purpose:     Decoder for binary-encoded structured data from DVT1 Current Meter modules
#
# Author:      evanShap
#
# Copyright:   (c) 2023 Sofar Ocean
# License:     Apache License, Version 2.0
# -------------------------------------------------------------------------------

import struct

# Struct description for Aanderaa Adapter DVT1 Firmware
DVT1_STRUCT_DESCRIPTION = [
    ('uint16_t', 'sample_count'),
    ('float', 'min'),
    ('float', 'max'),
    ('float', 'mean'),
    ('float', 'stdev'),
]

# Anderaa Adapter DVT1 Data Channels
DVT1_DATA_CHANNELS = [
    "Abs Speed[cm/s]",
    "Direction[Deg.M]",
    "North[cm/s]",
    "East[cm/s]",
    "Heading[Deg.M]",
    "Tilt X[Deg]",
    "Tilt Y[Deg]",
    "Ping Count",
    "Abs Tilt[Deg]"
]

# Anderaa Adapter Beta 2 Data Channels
BETA_2_DATA_CHANNELS = [
    "Abs Speed[cm/s]",
    "Direction[Deg.M]",
    "Abs Tilt[Deg]"
]

# Sample Hex Payload
SAMPLE_HEX_DATA = (
    "b1005abdf33fae96cb43b261f042f4199442b100784ecc3bf7acb343b71f48432059e042"
    "b100f938a2c37c39c843b7421c409192fe42b10034d20ac3c9561143cd137a41cedf6b42"
    "b100134f614244296742474364425cf1763eb10054d404422a34054291060542dc74993c"
    "b100b88951c2272251c2135351c2c2a8993cb1000000504100007041e2a45e410c1f023f"
    "b10002ec8e42d47b8f425c388f42e1f73b3d"
)

def get_struct_size_bytes(struct_description):
    """Calculate the size in bytes of a struct based on its description."""
    size_bytes = 0
    for element in struct_description:
        data_type = element[0]
        if data_type in ['uint16_t', 'int16_t']:
            size_bytes += 2
        elif data_type in ['float', 'uint32_t', 'int32_t']:
            size_bytes += 4
        elif data_type in ['double', 'uint64_t', 'int64_t']:
            size_bytes += 8
        else:
            raise ValueError(f"Unsupported struct data type!: {data_type}")
    return size_bytes

def hex_to_struct(hex_data, struct_description):
    """Convert hex payload to a dictionary of unpacked struct values."""
    byte_data = bytes.fromhex(hex_data.strip())
    format_string = '<'
    for data_type, _ in struct_description:
        if data_type == 'uint16_t':
            format_string += 'H'
        elif data_type == 'double':
            format_string += 'd'
        elif data_type == 'float':
            format_string += 'f'
        else:
            raise ValueError(f"Unsupported data type: {data_type}")

    expected_size = struct.calcsize(format_string)
    if len(byte_data) != expected_size:
        raise ValueError(f"Expected {expected_size} bytes, but got {len(byte_data)} bytes")

    values = struct.unpack(format_string, byte_data)
    result = {name: value for (_, name), value in zip(struct_description, values)}

    return result

def print_decoded_struct(decoded_data):
    """Pretty prints decoded structured data."""
    for data_channel in decoded_data:
        print(f"{data_channel['channel_name']}:")
        for element in data_channel['data']:
            print(f"\t{element}: {data_channel['data'][element]}")
        print("\n")

def decode_payload_to_structs(hex_payload, data_channels, struct_description):
    """Decode hex payload to structs based on the data channels and struct description."""
    decoded_structs = []
    struct_size_bytes = get_struct_size_bytes(struct_description)
    struct_hex_len = 2 * struct_size_bytes
    hex_payload_trimmed = hex_payload.replace(" ", "").replace("\n", "")
    if len(hex_payload_trimmed) % struct_hex_len != 0:
        raise ValueError(f"struct hex length {struct_hex_len} does not evenly divide into hex payload {hex_payload_trimmed}")
    for i in range(len(data_channels)):
        decoded_structs.append({
            'data': hex_to_struct(hex_payload_trimmed[i * struct_hex_len:(i + 1) * struct_hex_len], struct_description),
            'channel_name': data_channels[i]
        })
    return decoded_structs


if __name__ == "__main__":
    decoded = decode_payload_to_structs(SAMPLE_HEX_DATA, DVT1_DATA_CHANNELS, DVT1_STRUCT_DESCRIPTION)
    print_decoded_struct(decoded)
