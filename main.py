# Author
# Version

import tkinter as tk
import tkinter.ttk as ttk
from time import sleep
from PIL import ImageTk, Image
import sys

import Initialise
import Manual
import Settings
import TilePrint
import Controls
import RuntimeState

from random import randint
import serial               # used for serial communications. came from <pip3.6 install pyserial>
import RR_CommandGenerator     # class developed to generate a limited number of TT robot commands
import time
import pickle


root = tk.Tk()
root.withdraw()
state = RuntimeState.RuntimeState()

# Setup main window
main_image = Image.open("C:\\Users\\Finlay\\Documents\\Images\\MAIN.jpg")
main_image_tk = ImageTk.PhotoImage(main_image)
background = tk.Toplevel(root, background='black', width=640, height=480)
background.title("PxlRT Studio")
background.geometry("640x480")

# Create 4 windows that can be displayed in the info panel
initialise_panel = Initialise.Initialise(background, state)
manual_panel = Manual.Manual(background, state)
settings_panel = Settings.Settings(background, state)
tileprint_panel = TilePrint.TilePrint(background, state)

# Create main controls
controls = Controls.Controls(background, initialise_panel, manual_panel, settings_panel, tileprint_panel, state)

root.mainloop()
