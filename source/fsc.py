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


def main(filename, mode="color"):
    # Check if the file exists
    if not os.path.isfile(filename):
        print(f"Error: The file '{filename}' does not exist.")
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
        gamma = 40,  # customized
        shadows = 0,
        highlights = 0,
        temp = 0,
        tint = 0,
        sat = 140,  # customized
        base_detect = 0,
        base_rgb = (255, 255, 255),
        remove_dust = False
    )

    # Perform operations with the file
    print(f"Processing file: {filename}")
    photo = RawProcessing(file_directory=filename, default_settings=default_settings, global_settings=default_settings)
    photo.load(full_res=True)
    photo.process(full_res=True)
    photo.export(replace_extension_with_jpg(filename))


if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Process a negative film scan with optional color modes.")
    parser.add_argument("filename", help="Path to the file to process")
    
    # Add mutually exclusive arguments for color and grayscale
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--color", action="store_true", help="Process the file in color mode (default)")
    group.add_argument("-g", "--grayscale", action="store_true", help="Process the file in grayscale mode")

    args = parser.parse_args()

    # Determine the mode
    if args.grayscale:
        mode = "grayscale"
    else:
        mode = "color"

    # Run the main function with the provided arguments
    main(args.filename, mode)
