import argparse
import os

#custom classes
from RawProcessing import RawProcessing

#logging
import logging

logger = logging.getLogger(__name__)
FORMAT = '%(asctime)s:::%(levelname)s:::%(message)s'
logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format=FORMAT)


# Function to create new filename
def replace_extension_with_jpg(file_path):
    """
    Replace the extension of a file with '.jpg'.

    Args:
        file_path (str): The original file path.

    Returns:
        str: The file path with the '.jpg' extension.
    """
    base_name, _ = os.path.splitext(file_path)
    return f"{base_name}.jpg"


def main(filename_red, filename_green, filename_blue, mode="color"):
    # Check if the file exists
    if not os.path.isfile(filename_red):
        print(f"Error: The file '{filename_red}' does not exist.")
        return
    if not os.path.isfile(filename_green):
        print(f"Error: The file '{filename_green}' does not exist.")
        return
    if not os.path.isfile(filename_blue):
        print(f"Error: The file '{filename_blue}' does not exist.")
        return

    # Prepare settings
    default_settings = dict(
        film_type = 1 if mode == "color" else 0,
        dark_threshold = 25,
        light_threshold = 100,
        border_crop = 1,
        flip = False,
        white_point = 0,
        black_point = 0,
        gamma = 0,  # default 0, customized 40
        shadows = 0,
        highlights = 0,
        temp = 0,
        tint = 0,
        sat = 100,  # default 100, customized 140
        base_detect = 0,
        base_rgb = (255, 255, 255),
        remove_dust = False
    )

    # Perform operations with the file
    print(f"Processing files: {filename_red}, {filename_green}, {filename_blue}")
    photo = RawProcessing(None, default_settings=default_settings, global_settings=default_settings, file_directory_red=filename_red, file_directory_green=filename_green, file_directory_blue=filename_blue)
    photo.load(full_res=True)
    photo.process(full_res=True)
    photo.export(replace_extension_with_jpg(filename_red))


if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Process a negative film scan consisting of 3 digitezed images, for red, green and blue backlight, with optional color modes.")
    parser.add_argument("filename_red", help="Path to the red bakclight file to process")
    parser.add_argument("filename_green", help="Path to the green bakclight file to process")
    parser.add_argument("filename_blue", help="Path to the blue bakclight file to process")
    
    # Add mutually exclusive arguments for color and grayscale
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--color", action="store_true", help="Process the file in color mode (default)")

    args = parser.parse_args()

    # Determine the mode
    mode = "color"  # default and only option

    # Run the main function with the provided arguments
    main(args.filename_red, args.filename_green, args.filename_blue, mode)
