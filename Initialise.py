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


class Initialise():
    def __init__(self, parent):
        background_image=Image.open("C:\\Users\\Victor\\Documents\\Images\\grey10_480x315.jpg")
        self.background_image_tk = ImageTk.PhotoImage(background_image)
        self.info_initialise = tk.Label(parent, image=self.background_image_tk, width=480, height=315)
        self.info_initialise.place(x=130, y=135)

        self.banner = tk.Label(self.info_initialise, text="Initialisation Control",
                               bg=background_clr, fg=foreground_clr_banner)
        self.banner.place(x=0, y=0)

        self.button_rehome_TT = tk.Button(self.info_initialise, text="Rehome TT",
                                          bg=background_clr, fg=foreground_clr_off,
                                          activebackground=foreground_clr_on,
                                          font=button_font,
                                          width=button_width)
        self.button_rehome_TT.place(x=40, y=20)

        self.button_rehome_PAL = tk.Button(self.info_initialise, text="Rehome PAL",
                                           bg=background_clr, fg=foreground_clr_off,
                                           activebackground=foreground_clr_on,
                                           font=button_font,
                                           width=button_width)
        self.button_rehome_PAL.place(x=40, y=70)

        self.button_Mag2PAL_near = tk.Button(self.info_initialise, text="Move Chute to Gripper",
                                             bg=background_clr, fg=foreground_clr,
                                             activebackground=foreground_clr_on,
                                             font=button_font,
                                             width=button_width)
        self.button_Mag2PAL_near.place(x=40, y=120)

        self.button_Mag2PAL_far = tk.Button(self.info_initialise, text="Move Chute to Magazine",
                                            bg=background_clr, fg=foreground_clr,
                                            activebackground=foreground_clr_on,
                                            font=button_font,
                                            width=button_width)
        self.button_Mag2PAL_far.place(x=40, y=170)

        self.mapping_frame = tk.Frame(self.info_initialise, width=400, height=80, bg=background_clr, bd=2, relief=tk.RAISED)
        self.mapping_frame.place(x=40, y=220)
        self.cartridge_label = tk.Label(self.mapping_frame, text="Cartridge Mapping",
                                        bg=background_clr, fg=foreground_clr)
        self.cartridge_label.place(x=20, y=20)
        self.cartridge_label_mapping = []
        self.cartridge_label_mapping_entry = []
        for i in range(8):
            self.cartridge_label_mapping.append(tk.Label(self.mapping_frame, text=i,
                                                         bg=background_clr, fg=foreground_clr,
                                                         font=mapping_font))
            self.cartridge_label_mapping_entry.append(tk.Entry(self.mapping_frame, width=1, font=mapping_font))
            self.cartridge_label_mapping[i].place(x=140 + i * 30, y=0)
            self.cartridge_label_mapping_entry[i].place(x=140 + i * 30, y=33)
