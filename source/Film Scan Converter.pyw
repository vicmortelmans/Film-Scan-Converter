import rawpy
import cv2
import numpy as np
import tkinter as tk
from PIL import Image
import multiprocessing
import ctypes
import os
import sys
import matplotlib.colors
import logging 

#Custom classes
from GUI import GUI


logger = logging.getLogger(__name__)
FORMAT = '%(asctime)s:::%(levelname)s:::%(message)s'
logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format=FORMAT)
   
if __name__ == '__main__':
    # Main function
    
    multiprocessing.freeze_support()
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

        def resource_path(relative_path):    
            try:       
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath('.')

            return os.path.join(base_path, relative_path)

        datafile = 'camera-roll.ico'
        if not hasattr(sys, 'frozen'):
            datafile = os.path.join(os.path.dirname(__file__), datafile)
        else:
            datafile = os.path.join(sys.prefix, datafile)
    except Exception as e:
        logger.exception(f"Exception: {e}")
        root = tk.Tk()
    else:
        root = tk.Tk()
        root.iconbitmap(default=resource_path(datafile))

    window = GUI(root)
    root.mainloop()
