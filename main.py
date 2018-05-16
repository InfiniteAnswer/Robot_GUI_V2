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


root = tk.Tk()
root.withdraw()
state = RuntmeState.RuntimeState()

# Setup main window
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
