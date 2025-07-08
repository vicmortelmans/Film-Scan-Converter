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
def replace_extension(file_path, file_format):
    """
    Replace the extension of a file with <file_format>.

    Args:
        file_path (str): The original file path.

    Returns:
        str: The file path with the <file_format> extension.
    """
    base_name, _ = os.path.splitext(file_path)
    return f"{base_name}.{file_format}"


def main(filename_red, filename_green, filename_blue, mode="colour", output_format="jpg"):
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

    if mode == "bw":
        film_type = 0
    elif mode == "colour":
        film_type = 1
    elif mode == "slide":
        film_type = 2
    elif mode == "crop":
        film_type = 3
    elif mode == "scientific":
        film_type = 4
    elif mode == "vignet":
        film_type = 5

    # Prepare settings
    default_settings = dict(
        film_type = film_type,
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
    photo.export(replace_extension(filename_red, output_format))


if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Process a negative film scan consisting of 3 digitezed images, for red, green and blue backlight, with optional colour modes.")

    # Argument 1: command
    parser.add_argument(
        'mode',
        choices=['bw', 'colour', 'slide', 'crop', 'vignet', 'scientific'],
        help='Type of processing to apply (bw, colour, slide, crop, vignet, scientific)'
    )

    # Argument 2: output format
    parser.add_argument(
        'output_format',
        choices=['jpg', 'tiff'],
        help='Output format (jpg or tiff)'
    )

    # Arguments 3-5: three file paths
    parser.add_argument(
        'filepaths',
        nargs=3,
        help='Three input file paths'
    )

    args = parser.parse_args()

    # Run the main function with the provided arguments
    main(args.filepaths[0], args.filepaths[1], args.filepaths[2], args.mode, args.output_format)
