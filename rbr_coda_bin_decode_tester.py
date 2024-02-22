# -------------------------------------------------------------------------------
# Name:        rbr_coda_bin_decode_tester.py
# Purpose:     Decoder for binary-encoded structured data from Feb '24 DVT RBR modules
#
# Author:      towynlin
#
# Copyright:   (c) 2024 Sofar Ocean
# License:     Apache License, Version 2.0
# -------------------------------------------------------------------------------

from lib.binary_decoder import decode_payload_to_structs, print_decoded_struct

RBR_CODA_STRUCT_DESCRIPTION = [
    ("uint16_t", "sample_count"),
    ("double", "min"),
    ("double", "max"),
    ("double", "mean"),
    ("double", "stdev"),
]

RBR_CODA_DATA_CHANNELS = [
    "Temperature[ºC] or Pressure[dbar]",
]

if __name__ == "__main__":
    user_input = input("Please enter the hex payload: ")
    decoded = decode_payload_to_structs(
        user_input, RBR_CODA_DATA_CHANNELS, RBR_CODA_STRUCT_DESCRIPTION
    )
    print_decoded_struct(decoded)
