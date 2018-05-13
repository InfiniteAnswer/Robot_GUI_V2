import tkinter as tk
import tkinter.ttk as ttk
from time import sleep
from PIL import ImageTk,Image
import sys

import Initialise
import Manual
import Settings



root = tk.Tk()
root.withdraw()
background = tk.Toplevel(root, background='black', width=640, height=480)
background.title("PxlRT Studio")
# background.wm_overrideredirect(True)
background.geometry("640x480")
# background_image=Image.open("C:\\Users\\Victor\\Documents\\Images\\cf_640x480.jpg")
# background_image_tk = ImageTk.PhotoImage(background_image)
# background_label = tk.Label(background, image=background_image_tk)
# background_label.place(x=0, y=0, relwidth=1, relheight=1)

tools_image=Image.open("C:\\Users\\Victor\\Documents\\Images\\Settings_small.jpg")
tools_image_tk = ImageTk.PhotoImage(tools_image)

manual_image=Image.open("C:\\Users\\Victor\\Documents\\Images\\Manual_small.jpg")
manual_image_tk = ImageTk.PhotoImage(manual_image)

print_image=Image.open("C:\\Users\\Victor\\Documents\\Images\\Print_small.jpg")
print_image_tk = ImageTk.PhotoImage(print_image)

initialise_image=Image.open("C:\\Users\\Victor\\Documents\\Images\\Initialise_small.jpg")
initialise_image_tk = ImageTk.PhotoImage(initialise_image)

PxlRT_image=Image.open("C:\\Users\\Victor\\Documents\\Images\\PxlRT_Studio4.jpg")
PxlRT_image_tk = ImageTk.PhotoImage(PxlRT_image)

tt_manual_image=Image.open("C:\\Users\\Victor\\Documents\\Images\\tt_manual.jpg")
tt_manual_image_tk = ImageTk.PhotoImage(tt_manual_image)

button_tools = tk.Button(background, image=tools_image_tk, bd=1, highlightthickness=0, relief=tk.RAISED)
button_tools.place(x=30,y=375)

button_manual = tk.Button(background, image=manual_image_tk, bd=1, highlightthickness=0, relief=tk.RAISED)
button_manual.place(x=30,y=295)

button_print = tk.Button(background, image=print_image_tk, bd=1, highlightthickness=0, relief=tk.RAISED)
button_print.place(x=30,y=215)

button_initialise = tk.Button(background, image=initialise_image_tk, bd=1, highlightthickness=0, relief=tk.RAISED)
button_initialise.place(x=30,y=135)

PxlRT_icon = tk.Label(background, image=PxlRT_image_tk, bd=0, highlightthickness=0, relief=tk.RAISED)
PxlRT_icon.place(x=30,y=30)




info = tk.Label(background, bg="grey10", image=tt_manual_image_tk, width=480, height=315)
info.place(x=130, y=135)


info_manual = tk.Label(background, bg="grey10", image=tt_manual_image_tk, width=480, height=315)
info_manual.place(x=130, y=135)

info_initialise = tk.Label(background, bg="grey10", width=480, height=315)
info_initialise.place(x=130, y=135)

info_settings = tk.Label(background, bg="grey10", width=480, height=315)
info_settings.place(x=130, y=135)

tt_mannual_ax1pp = tk.Button(info, text="+", bg="red", font=("Courier", 18))
tt_mannual_ax1pp.place(x=10,y=210)
tt_mannual_ax1mm = tk.Button(info, text="-", bg="red", font=("Courier", 18))
tt_mannual_ax1mm.place(x=130,y=230)

tt_mannual_ax4pp = tk.Button(info, text="+", bg="yellow", font=("Courier", 18))
tt_mannual_ax4pp.place(x=310,y=255)
tt_mannual_ax4mm = tk.Button(info, text="-", bg="yellow", font=("Courier", 18))
tt_mannual_ax4mm.place(x=380,y=270)

tt_mannual_ax2pp = tk.Button(info, text="+", bg="green", font=("Courier", 18))
tt_mannual_ax2pp.place(x=75,y=75)
tt_mannual_ax2mm = tk.Button(info, text="-", bg="green", font=("Courier", 18))
tt_mannual_ax2mm.place(x=120,y=50)

tt_mannual_ax3pp = tk.Button(info, text="+", bg="blue", font=("Courier", 18))
tt_mannual_ax3pp.place(x=230,y=125)
tt_mannual_ax3mm = tk.Button(info, text="-", bg="blue", font=("Courier", 18))
tt_mannual_ax3mm.place(x=230,y=25)

tt_manual_ax1tt = tk.Label(info, text="x=300/400", bg="black", fg="red")
tt_manual_ax1tt.place(x=400,y=70)
tt_manual_ax2tt = tk.Label(info, text="x=300/400", bg="black", fg="green")
tt_manual_ax2tt.place(x=400,y=100)
tt_manual_ax3tt = tk.Label(info, text="x=300/100", bg="black", fg="blue")
tt_manual_ax3tt.place(x=400,y=130)
tt_manual_ax4tt = tk.Label(info, text="x=300/100", bg="black", fg="yellow")
tt_manual_ax4tt.place(x=400,y=160)
tt_mannual_speed = tk.Scale(info, from_=1, to=3, resolution=1, orient=tk.HORIZONTAL,
                            label="speed",
                            bd=0, highlightthickness=0, fg="yellow", bg="black", length=80)
tt_mannual_speed.place(x=390,y=15)

info.place_forget()
# info2.place_forget()


dummyframe=tk.Frame(background, bg="grey10", width=480, height=315)
dummyframe.place(x=130, y=135)

vscrollbar = tk.Scrollbar(dummyframe, orient=tk.VERTICAL, troughcolor="red")
vscrollbar.grid(row=0, column=1, sticky=tk.N + tk.S)

c=tk.Canvas(dummyframe, width=400, height=315, yscrollcommand=vscrollbar.set, scrollregion=(0,0,1000,1000))
c.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
#
#
#

param_pal = tk.Frame(c, bg="grey10")
param_pal.place(x=0, y=0)
# tk.Label(param_pal, text="oops").pack()
for i in range(30):
    tk.Label(param_pal, text = i, fg="yellow", bg="black").grid(row=i)
    tk.Entry(param_pal, fg="black").grid(row=i, column=1)

id = c.create_window(10,0, anchor=tk.NW, window=param_pal)

vscrollbar.config(command=c.yview)

dummyframe.place_forget()

iw= Initialise.Initialise(info_initialise)
info_initialise.place_forget()

mw = Manual.Manual(info_manual)
info_manual.place_forget()

sw = Settings.Settings(background)

root.mainloop()