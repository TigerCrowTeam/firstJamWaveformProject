import numpy as np
from PIL import Image

def image_to_interleaved_binary_array(image_path, output_file):
    """
    Reads a JPG image, converts its RGB pixel values to an interleaved array
    of ones and zeros, saves it to a file, and returns image dimensions.

    Args:
        image_path (str): The path to the JPG image file.
        output_file (str): The path to the output file for Gnu Radio.

    Returns:
        tuple: A tuple containing:
            - rows (int): The number of rows (height) of the image.
            - cols (int): The number of columns (width) of the image.
    """
    try:
        img = Image.open(image_path).convert('RGB')
        img_array = np.array(img)
        rows, cols, channels = img_array.shape
        binary_list = []
        for row in img_array:
            for pixel in row:
                for color_value in pixel:
                    binary_representation = format(color_value, '08b')
                    for bit in binary_representation:
                        binary_list.extend([int(bit)] * 8)
                        

        # Interleave zeroes
        interleaved_list = []
        for val in binary_list:
            interleaved_list.append(float(val)*2-1)
            interleaved_list.append(0.0)

        interleaved_array = np.array(interleaved_list, dtype=np.float32)

        # Save to file for Gnu Radio
        interleaved_array.tofile(output_file)

        return rows, cols, binary_list

    except FileNotFoundError:
        print(f"Error: Image file not found at '{image_path}'")
        return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

if __name__ == '__main__':
    image_file = 'inputPic1.bmp'  # Replace with the actual path to your JPG image
    output_filename = 'inputPic1.bin'  # Name of the output file for Gnu Radio

    num_rows, num_cols, bitlist = image_to_interleaved_binary_array(image_file, output_filename)

    if num_rows is not None:
        print(f"Image processed successfully.")
        print(f"Number of rows: {num_rows}")
        print(f"Number of columns: {num_cols}")
        print(f"Interleaved binary data saved to '{output_filename}' as floating point numbers.")
    else:
        print(f"Could not process the image at '{image_file}'. Please ensure the file exists and is a valid JPG image.")