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


class Manual():
    def __init__(self, parent):
        self.tt_mannual_ax1pp = tk.Button(parent, text="+", bg="red", font=("Courier", 18))
        self.tt_mannual_ax1pp.place(x=10,y=210)
        self.tt_mannual_ax1mm = tk.Button(parent, text="-", bg="red", font=("Courier", 18))
        self.tt_mannual_ax1mm.place(x=130,y=230)
        
        self.tt_mannual_ax4pp = tk.Button(parent, text="+", bg="yellow", font=("Courier", 18))
        self.tt_mannual_ax4pp.place(x=310,y=255)
        self.tt_mannual_ax4mm = tk.Button(parent, text="-", bg="yellow", font=("Courier", 18))
        self.tt_mannual_ax4mm.place(x=380,y=270)
        
        self.tt_mannual_ax2pp = tk.Button(parent, text="+", bg="green", font=("Courier", 18))
        self.tt_mannual_ax2pp.place(x=75,y=75)
        self.tt_mannual_ax2mm = tk.Button(parent, text="-", bg="green", font=("Courier", 18))
        self.tt_mannual_ax2mm.place(x=120,y=50)
        
        self.tt_mannual_ax3pp = tk.Button(parent, text="+", bg="blue", font=("Courier", 18))
        self.tt_mannual_ax3pp.place(x=230,y=125)
        self.tt_mannual_ax3mm = tk.Button(parent, text="-", bg="blue", font=("Courier", 18))
        self.tt_mannual_ax3mm.place(x=230,y=25)
        
        self.tt_manual_ax1tt = tk.Label(parent, text="x=300/400", bg="black", fg="red")
        self.tt_manual_ax1tt.place(x=400,y=70)
        self.tt_manual_ax2tt = tk.Label(parent, text="x=300/400", bg="black", fg="green")
        self.tt_manual_ax2tt.place(x=400,y=100)
        self.tt_manual_ax3tt = tk.Label(parent, text="x=300/100", bg="black", fg="blue")
        self.tt_manual_ax3tt.place(x=400,y=130)
        self.tt_manual_ax4tt = tk.Label(parent, text="x=300/100", bg="black", fg="yellow")
        self.tt_manual_ax4tt.place(x=400,y=160)
        self.tt_mannual_speed = tk.Scale(parent, from_=1, to=3, resolution=1, orient=tk.HORIZONTAL,
                                    label="speed",
                                    bd=0, highlightthickness=0, fg="yellow", bg="black", length=80)
        self.tt_mannual_speed.place(x=390,y=15)