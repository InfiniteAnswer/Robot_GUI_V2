import tkinter as tk
import tkinter.ttk as ttk
from time import sleep
from PIL import ImageTk, Image
import sys

import Initialise
import Manual
import Settings


class Controls():
    def __init__(self, background, initialise_panel, manual_panel, settings_panel, tileprint_panel, state):
        self.background = background
        self.initialise_panel = initialise_panel
        self.manual_panel = manual_panel
        self.settings_panel = settings_panel
        self.tileprint_panel = tileprint_panel
        self.state = state

        # Define control flags
        self.flag_homeax1 = False
        self.flag_homeax2 = False
        self.flag_homeax3 = False
        self.flag_homeax4 = False
        self.flag_printing = False
        self.flag_magazineinitialised = False
        self.flag_paletteinitialised = False
        self.flag_fileloaded = False
        self.flag_printpause = False

        # Create blank grey default info panel
        background_image = Image.open(self.state.path + "Images\\480x315_BLACK.jpg")
        self.background_image_tk = ImageTk.PhotoImage(background_image)
        self.info_controls = tk.Label(background, image=self.background_image_tk, width=480, height=315)
        self.info_controls.place(x=130, y=135)

        # Define images for 4 main buttons, header banner, and overall system outline
        settings_image = Image.open(self.state.path + "Images\\SETTINGS_BUTTON.jpg")
        self.settings_image_tk = ImageTk.PhotoImage(settings_image)

        manual_image = Image.open(self.state.path + "Images\\MANUAL_BUTTON.jpg")
        self.manual_image_tk = ImageTk.PhotoImage(manual_image)

        print_image = Image.open(self.state.path + "Images\\PRINT_BUTTON.jpg")
        self.print_image_tk = ImageTk.PhotoImage(print_image)

        initialise_image = Image.open(self.state.path + "Images\\INITIALISE_BUTTON.jpg")
        self.initialise_image_tk = ImageTk.PhotoImage(initialise_image)

        PxlRT_image = Image.open(self.state.path + "Images\\BANNER.jpg")
        self.PxlRT_image_tk = ImageTk.PhotoImage(PxlRT_image)

        # tt_manual_image = Image.open("C:\\Users\\Finlay\\Documents\\Images\\tt_manual.jpg")
        # self.tt_manual_image_tk = ImageTk.PhotoImage(tt_manual_image)
        #
        # Add logo and banner to background
        self.PxlRT_icon = tk.Label(self.background, image=self.PxlRT_image_tk, bd=0, highlightthickness=0,
                                   relief=tk.RAISED)
        self.PxlRT_icon.place(x=0, y=10)

        # Create 4 main buttons
        self.button_settings = tk.Button(self.background, image=self.settings_image_tk, bd=1,
                                         command=self.callback_settings,
                                         highlightthickness=0, relief=tk.RAISED)
        self.button_settings.place(x=30, y=375)

        self.button_manual = tk.Button(self.background, image=self.manual_image_tk, bd=1, highlightthickness=0,
                                       relief=tk.RAISED,
                                       command=self.callback_manual)
        self.button_manual.place(x=30, y=295)

        self.button_print = tk.Button(self.background, image=self.print_image_tk, bd=1, highlightthickness=0,
                                      command=self.callback_print,
                                      relief=tk.RAISED)
        self.button_print.place(x=30, y=215)

        self.button_initialise = tk.Button(self.background, image=self.initialise_image_tk, bd=1,
                                           command=self.callback_initialise,
                                           highlightthickness=0, relief=tk.RAISED)
        self.button_initialise.place(x=30, y=135)

        # Bring initialisation info panel to front as default start display
        initialise_panel.info_initialise.lift(aboveThis=None)

    def callback_manual(self):
        self.manual_panel.info_manual.lift(aboveThis=None)

    def callback_print(self):
        self.tileprint_panel.info_tileprint.lift(aboveThis=None)

    def callback_initialise(self):
        self.initialise_panel.info_initialise.lift(aboveThis=None)

    def callback_settings(self):
        self.settings_panel.info_settings.lift(aboveThis=None)
