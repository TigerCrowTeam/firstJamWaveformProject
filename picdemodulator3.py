#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  1 08:51:00 2025

@author: abel
"""

import sys
import struct
import numpy as np
from PIL import Image

import numpy as np

def process_binary_file(bin_filepath):


    with open(bin_filepath, 'rb') as f:
        data = f.read()
    if not data:
        return np.array([])
    datax= np.array(list(data[i] for i in range(0, len(data), 1)), dtype=np.uint8)

    
    
    
    
    num_rows=len(datax)//8
    datax=datax.reshape(num_rows,8)
    row_sums = np.sum(datax, axis=1)


    # Create the final array based on the condition (sum > 4)
    final_array = np.where(row_sums > 4, 1, 0).astype(np.uint8)

    return final_array



    
def numpy_to_color_bmp(numpy_array, rows, cols, bmp_filepath):
    """
    Takes a NumPy array of ones and zeros and creates a color .bmp image.

    Interprets the NumPy array by taking groups of 24 consecutive bits
    to represent the 8-bit Red, Green, and Blue color values for each pixel.

    Args:
        numpy_array (numpy.ndarray): A 1D NumPy array containing only ones and zeros.
        rows (int): The desired number of rows in the output image.
        cols (int): The desired number of columns in the output image.
        bmp_filepath (str): The path to save the output .bmp file.
    """
    total_bits = numpy_array.size
    expected_bits = rows * cols * 24

    if total_bits != expected_bits:
        raise ValueError(
            f"The NumPy array size ({total_bits}) does not match the expected "
            f"size for {rows}x{cols} pixels (each 24 bits): {expected_bits} bits."
        )

    pixels = []
    bit_index = 0
    for _ in range(rows * cols):
        r_bits = numpy_array[bit_index:bit_index + 8]
        g_bits = numpy_array[bit_index + 8:bit_index + 16]
        b_bits = numpy_array[bit_index + 16:bit_index + 24]

        r = int("".join(map(str, r_bits)), 2)
        g = int("".join(map(str, g_bits)), 2)
        b = int("".join(map(str, b_bits)), 2)

        pixels.append((r, g, b))
        bit_index += 24

    try:
        image = Image.new('RGB', (cols, rows))
        image.putdata(pixels)
        image.save(bmp_filepath)
        print(f"Successfully created {bmp_filepath} from the NumPy array.")
    except Exception as e:
        print(f"An error occurred while saving the image: {e}")
        
X=process_binary_file("outputPic1.bin")
numpy_to_color_bmp(X, 400, 300, "outputPic1.bmp")
