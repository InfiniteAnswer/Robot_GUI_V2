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


class TilePrint():
    def __init__(self, parent, state):
        self.state = state
        background_image = Image.open("C:\\Users\\Victor\\Documents\\Images\\grey10_480x315.jpg")
        self.background_image_tk = ImageTk.PhotoImage(background_image)
        self.info_tileprint = tk.Label(parent, image=self.background_image_tk, width=480, height=315)
        self.info_tileprint.place(x=130, y=135)

        self.banner = tk.Label(self.info_tileprint, text="Print Control",
                               bg=background_clr, fg=foreground_clr_banner)
        self.banner.place(x=0, y=0)

        self.button_loadfile = tk.Button(self.info_tileprint, text="Load File",
                                          bg=background_clr, fg=foreground_clr_off,
                                          activebackground=foreground_clr_on,
                                          font=button_font,
                                          width=button_width)
        self.button_loadfile.place(x=40, y=20)

        self.button_start = tk.Button(self.info_tileprint, text="Start",
                                           bg=background_clr, fg=foreground_clr_off,
                                           activebackground=foreground_clr_on,
                                           font=button_font,
                                           width=button_width)
        self.button_start.place(x=40, y=70)

        self.button_pause = tk.Button(self.info_tileprint, text="Pause",
                                             bg=background_clr, fg=foreground_clr,
                                             activebackground=foreground_clr_on,
                                             font=button_font,
                                             width=button_width)
        self.button_pause.place(x=40, y=120)

        self.button_abort = tk.Button(self.info_tileprint, text="Abort",
                                            bg=background_clr, fg=foreground_clr,
                                            activebackground=foreground_clr_on,
                                            font=button_font,
                                            width=button_width)
        self.button_abort.place(x=40, y=170)

        self.print_speed = tk.Scale(self.info_tileprint, from_=10, to=100, resolution=10, orient=tk.HORIZONTAL,
                                    label="% of Max Speed",
                                    bd=0, highlightthickness=0, fg="yellow", bg="grey10", length=400)
        self.print_speed.place(x=40,y=220)
