
from tkinter import ttk
import tkinter as tk
import logging 


logger = logging.getLogger(__name__)
FORMAT = '%(asctime)s:::%(levelname)s:::%(message)s'
logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format=FORMAT)

class AutoScrollbar(ttk.Scrollbar):
   # A scrollbar that hides itself if it's not needed.
   # Only works if you use the grid geometry manager!
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call('grid', 'remove', self)
        else:
            self.grid()
        ttk.Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise tk.TclError('cannot use pack with this widget')
    def place(self, **kw):
        raise tk.TclError('cannot use place with this widget')
