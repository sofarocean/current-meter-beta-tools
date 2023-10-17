# -------------------------------------------------------------------------------
# Name:        bm_decode_tester.py
# Purpose:     Decoder for binary-encoded structured data from DVT1 Current Meter modules
#
# Author:      evanShap
#
# Copyright:   (c) 2023 Sofar Ocean
# License:     Apache License, Version 2.0
# -------------------------------------------------------------------------------

from lib.binary_decoder import decode_payload_to_structs, print_decoded_struct, DVT1_DATA_CHANNELS, DVT1_STRUCT_DESCRIPTION

if __name__ == "__main__":
    user_input = input("Please enter the hex payload: ")
    decoded = decode_payload_to_structs(user_input, DVT1_DATA_CHANNELS, DVT1_STRUCT_DESCRIPTION)
    print_decoded_struct(decoded)