#!/usr/bin/env python3
#
# Copyright (c) 2021-2022 LISTENAI
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

from headerutil import HEADER_SIZE, patch_header, fill_header_tag

def patch_bin(filename:str):
    with open(filename, 'rb+') as bin_file:
        header = bytearray(bin_file.read(HEADER_SIZE))
        fill_header_tag(header)
        image_size = os.path.getsize(filename)
        patch_header(header, image_size)
        bin_file.seek(0, 0)
        bin_file.write(header)
        print(f'csk6 rom boot tag add successfully, file:{filename}')

def main():
    patch_bin(sys.argv[1])

if __name__ == "__main__":
    main()
