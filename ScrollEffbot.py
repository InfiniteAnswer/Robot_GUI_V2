from tkinter import *

root = Tk()

# f=Canvas(root, width=100, height=100)
# f.place(x=0, y=0)
# scrollbar = Scrollbar(f)
# scrollbar.pack(side=RIGHT, fill=Y)
#
# # listbox = Listbox(f)
# # listbox.pack()
# #
# # for i in range(100):
# #     listbox.insert(END, i)
#
# listbox = Canvas(f,width=500, height=500, bg="blue", scrollregion=(0,0,500,500))
# listbox.pack()
#
#
# # attach listbox to scrollbar
# listbox.config(yscrollcommand=scrollbar.set)
# scrollbar.config(command=listbox.yview)


frame=Frame(root,width=300,height=300)
frame.grid(row=0,column=0)
canvas=Canvas(frame,bg='#FFFFFF',width=300,height=300,scrollregion=(0,0,500,500))
hbar=Scrollbar(frame,orient=HORIZONTAL)
hbar.pack(side=BOTTOM,fill=X)
hbar.config(command=canvas.xview)
vbar=Scrollbar(frame,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y)
vbar.config(command=canvas.yview)
canvas.config(width=300,height=300)
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
canvas.pack(side=LEFT,expand=True,fill=BOTH)



mainloop()