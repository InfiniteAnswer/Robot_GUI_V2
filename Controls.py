import tkinter as tk
import tkinter.ttk as ttk
from time import sleep
from PIL import ImageTk,Image
import sys

import Initialise
import Manual
import Settings

class Controls():
    def __init__(self, background, info_manual):
        self.background=background
        self.info_manual = info_manual
        self.manual_state = tk.BooleanVar()
        self.manual_state.set(0)
        self.print_state = tk.BooleanVar()
        self.print_state.set(0)
        self.settings_state = tk.BooleanVar()
        self.settings_state.set(0)
        self.initialise_state = tk.BooleanVar()
        self.initialise_state.set(0)

        settings_image=Image.open("C:\\Users\\Victor\\Documents\\Images\\Settings_small.jpg")
        self.settings_image_tk = ImageTk.PhotoImage(settings_image)

        manual_image=Image.open("C:\\Users\\Victor\\Documents\\Images\\Manual_small.jpg")
        self.manual_image_tk = ImageTk.PhotoImage(manual_image)

        print_image=Image.open("C:\\Users\\Victor\\Documents\\Images\\Print_small.jpg")
        self.print_image_tk = ImageTk.PhotoImage(print_image)

        initialise_image=Image.open("C:\\Users\\Victor\\Documents\\Images\\Initialise_small.jpg")
        self.initialise_image_tk = ImageTk.PhotoImage(initialise_image)

        PxlRT_image=Image.open("C:\\Users\\Victor\\Documents\\Images\\PxlRT_Studio4.jpg")
        self.PxlRT_image_tk = ImageTk.PhotoImage(PxlRT_image)

        tt_manual_image=Image.open("C:\\Users\\Victor\\Documents\\Images\\tt_manual.jpg")
        self.tt_manual_image_tk = ImageTk.PhotoImage(tt_manual_image)

        self.button_settings = tk.Button(background, image=self.settings_image_tk, bd=1,
                                      command=self.callback_settings,
                                      highlightthickness=0, relief=tk.RAISED)
        self.button_settings.place(x=30,y=375)

        self.button_manual = tk.Button(background, image=self.manual_image_tk, bd=1, highlightthickness=0,
                                       relief=tk.RAISED,
                                       command=self.callback_manual)
        self.button_manual.place(x=30,y=295)

        self.button_print = tk.Button(background, image=self.print_image_tk, bd=1, highlightthickness=0,
                                      command=self.callback_print,
                                      relief=tk.RAISED)
        self.button_print.place(x=30,y=215)

        self.button_initialise = tk.Button(background, image=self.initialise_image_tk, bd=1,
                                           command=self.callback_initialise,
                                           highlightthickness=0, relief=tk.RAISED)
        self.button_initialise.place(x=30,y=135)

        self.PxlRT_icon = tk.Label(background, image=self.PxlRT_image_tk, bd=0,highlightthickness=0, relief=tk.RAISED)
        self.PxlRT_icon.place(x=30,y=30)


    def callback_manual(self):
        if (self.manual_state.get() == 0):
            self.manual_state.set(1)
            self.initialise_state.set(0)
            self.print_state.set(0)
            self.settings_state.set(0)
            self.info_manual.place(x=130, y=135)
            self.info_manual.lift(aboveThis=None)
        else:
            self.manual_state.set(0)

    def callback_print(self):
        if (self.print_state.get() == 0):
            self.manual_state.set(0)
            self.initialise_state.set(0)
            self.print_state.set(1)
            self.settings_state.set(0)
        else:
            self.print_state.set(0)

    def callback_initialise(self):
        if (self.initialise_state.get() == 0):
            self.manual_state.set(0)
            self.initialise_state.set(1)
            self.print_state.set(0)
            self.settings_state.set(0)
        else:
            self.initialise_state.set(0)

    def callback_settings(self):
        if (self.settings_state.get() == 0):
            self.manual_state.set(0)
            self.initialise_state.set(0)
            self.print_state.set(0)
            self.settings_state.set(1)
        else:
            self.settings_state.set(0)