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
import Controls


def callback_manual(*args):
    # if (controls.manual_state.get() == 1):
    #     info_manual.place(x=130, y=135)
    #     info_initialise.place_forget()
    #     sw.dummyframe.place_forget()
    #     controls.button_manual.config(relief=tk.SUNKEN)
    # elif (controls.initialise_state.get() == 1):
    #     info_manual.place_forget()
    #     info_initialise.place(x=130, y=135)
    #     sw.dummyframe.place_forget()
    #     controls.button_initialise.config(relief=tk.SUNKEN)
    # elif (controls.settings_state.get() == 1):
    #     info_manual.place_forget()
    #     info_initialise.place_forget()
    #     sw.dummyframe.place(x=130, y=135)
    #     controls.button_settings.config(relief=tk.SUNKEN)
    # else:
    #     info_initialise.place_forget()
    #     sw.dummyframe.place_forget()
    #     info_manual.place_forget()
    if (controls.manual_state.get() == 1):
        # info_manual.lift(aboveThis=None)
        pass
    elif (controls.initialise_state.get() == 1):
        info_initialise.lift(aboveThis=None)
    elif (controls.settings_state.get() == 1):
        sw.dummyframe.lift(aboveThis=None)

root = tk.Tk()
root.withdraw()
background = tk.Toplevel(root, background='black', width=640, height=480)
background.title("PxlRT Studio")
background.geometry("640x480")

# controls = Controls.Controls(background)

info_initialise = tk.Label(background, bg="grey10", width=480, height=315)
info_initialise.place(x=130, y=135)

tt_manual_image = Image.open("C:\\Users\\Victor\\Documents\\Images\\tt_manual.jpg")
tt_manual_image_tk = ImageTk.PhotoImage(tt_manual_image)
info_manual = tk.Label(background, bg="grey10", image=tt_manual_image_tk, width=480, height=315)
info_manual.place(x=130, y=135)

iw = Initialise.Initialise(info_initialise)
# info_initialise.place_forget()
info_initialise.place(x=130, y=135)

mw = Manual.Manual(info_manual)
info_manual.place_forget()
# info_manual.place(x=130, y=135)

sw = Settings.Settings(background)
# sw.dummyframe.place_forget()

controls = Controls.Controls(background, info_manual)

controls.manual_state.trace("w", callback_manual)
controls.initialise_state.trace("w", callback_manual)
controls.settings_state.trace("w", callback_manual)

root.mainloop()
