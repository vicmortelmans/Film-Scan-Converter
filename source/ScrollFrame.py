import platform
import tkinter as tk
from tkinter import ttk
import logging 

#Custom classes
from AutoScrollbar import AutoScrollbar


logger = logging.getLogger(__name__)
FORMAT = '%(asctime)s:::%(levelname)s:::%(message)s'
logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format=FORMAT)

class ScrollFrame:
    def __init__(self, master):
        self.vscrollbar = AutoScrollbar(master)
        self.vscrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)
        self.hscrollbar = AutoScrollbar(master, orient=tk.HORIZONTAL)
        self.hscrollbar.grid(row=1, column=0, sticky=tk.E+tk.W)

        self.canvas = tk.Canvas(master, yscrollcommand=self.vscrollbar.set, xscrollcommand=self.hscrollbar.set, takefocus=0, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        self.vscrollbar.config(command=self.canvas.yview)
        self.hscrollbar.config(command=self.canvas.xview)

        # make the canvas expandable
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        # create frame inside canvas
        self.frame = ttk.Frame(self.canvas)
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(1, weight=1)

        self.frame.bind('<Configure>', self.reset_scrollregion)
        self.frame.bind('<Enter>', lambda _: self.frame.bind_all('<MouseWheel>', self._on_mousewheel))
        self.frame.bind('<Leave>', lambda _: self.frame.unbind_all('<MouseWheel>'))

    def update(self):
        self.canvas.create_window(0, 0, anchor=tk.NW, window=self.frame)
        self.frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox('all'))

        if self.frame.winfo_reqwidth() != self.canvas.winfo_width():
            # update the canvas's width to fit the inner frame
            self.canvas.config(width = self.frame.winfo_reqwidth())
        if self.frame.winfo_reqheight() != self.canvas.winfo_height():
            # update the canvas's height to fit the inner frame
            self.canvas.config(height = self.frame.winfo_reqheight())
    
    def reset_scrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
    
    def _on_mousewheel(self, event):
        # binding mousewheel event to scrolling
        caller = event.widget
        if not (isinstance(caller, ttk.Spinbox) or isinstance(caller, ttk.Combobox)): # ignore scrolling on spinboxes and comboboxes
            if platform.system() == 'Windows': # setting different scrolling speeds based on platform
                delta_scale = 120
            else:
                delta_scale = 1
            if (self.frame.winfo_reqheight() > self.canvas.winfo_height()):
                self.canvas.yview_scroll(int(-1*(event.delta/delta_scale)), 'units')
