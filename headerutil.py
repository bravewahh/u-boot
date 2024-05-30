#!/usr/bin/env python3
#
# Copyright (c) 2021-2022 LISTENAI
#
# SPDX-License-Identifier: Apache-2.0

# Define the image header using bytearray for mutable bytes
image_header_tag = bytearray([
    ord('H'), ord('r'),                # Header mark "Hr"
    0x01, 0x00,                        # Version 1.0
    0x00, 0x00, 0x00, 0x00,            # Image size (placeholder)
    0x00, 0x00, 0x00, 0x18,            # "__Vectors", image VMA
    0x01, 0x00, 0x00, 0x00, 
    *b'VENUS_RTOS', 0x00               # Image name "VENUS_RTOS" with null termination
] + [0x00] * 22)                       # Fill the rest of the array with 0s to reach 48 bytes total

_IMAGE_START = 192
_IMAGE_SIZE_OFFSET = _IMAGE_START + 4
_IMAGE_HDR_CHK_OFFSET = _IMAGE_START + 60

HEADER_SIZE = _IMAGE_HDR_CHK_OFFSET + 4

def fill_header_tag(header_bytes: bytearray):
    start_index = _IMAGE_START
    end_index = start_index + len(image_header_tag)
    header_bytes[start_index:end_index] = image_header_tag

def _get_header_sum(header_bytes: bytearray):
    header_sum = 0
    for pos in range(_IMAGE_START, _IMAGE_HDR_CHK_OFFSET):
        header_sum += header_bytes[pos]

    vector_sum = 0
    for pos in range(_IMAGE_HDR_CHK_OFFSET):
        vector_sum += header_bytes[pos]
    vector_sum += (header_sum) & 0xff
    vector_sum += (header_sum >> 8) & 0xff

    return header_sum, vector_sum

def patch_header(header_bytes: bytearray, image_size: int):
    header_bytes[_IMAGE_SIZE_OFFSET:_IMAGE_SIZE_OFFSET + 4] = image_size.to_bytes(4, 'little')

    header_sum, vector_sum = _get_header_sum(header_bytes)
    header_bytes[_IMAGE_HDR_CHK_OFFSET + 0:_IMAGE_HDR_CHK_OFFSET + 2] = header_sum.to_bytes(2, 'little')
    header_bytes[_IMAGE_HDR_CHK_OFFSET + 2:_IMAGE_HDR_CHK_OFFSET + 4] = vector_sum.to_bytes(2, 'little')
