import tkinter as tk
import tkinter.ttk as ttk
from time import sleep
from PIL import ImageTk, Image
import sys

background_clr = "grey10"
foreground_clr = "yellow"
foreground_clr_off = "red"
foreground_clr_on = "green"
foreground_clr_banner = "grey50"
# button_font = ("Arial", 18)
button_font = "Arial 16 bold"
mapping_font = "Arial 16"
button_width = 30


class Settings():
    def __init__(self, parent, state):
        self.state = state
        background_image = Image.open(self.state.path + "Images\\480x315_BLACK.jpg")
        self.background_image_tk = ImageTk.PhotoImage(background_image)
        self.info_settings = tk.Label(parent, image=self.background_image_tk, width=480, height=315)
        self.info_settings.place(x=130, y=135)

        self.dummyframe = tk.Frame(self.info_settings, bg="grey10", width=480, height=315)
        self.dummyframe.place(x=0, y=0)

        self.vscrollbar = tk.Scrollbar(self.dummyframe, orient=tk.VERTICAL, troughcolor="red")
        self.vscrollbar.grid(row=0, column=1, sticky=tk.N + tk.S)

        self.canvas = tk.Canvas(self.dummyframe, width=400, height=315, yscrollcommand=self.vscrollbar.set,
                                scrollregion=(0, 0, 1000, 1000))
        self.canvas.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        self.param_pal = tk.Frame(self.canvas, bg="grey10")
        self.param_pal.place(x=0, y=0)

        for i in range(30):
            tk.Label(self.param_pal, text=i, fg="yellow", bg="black").grid(row=i)
            tk.Entry(self.param_pal, fg="black").grid(row=i, column=1)

        self.id = self.canvas.create_window(10, 0, anchor=tk.NW, window=self.param_pal)

        self.vscrollbar.config(command=self.canvas.yview)
