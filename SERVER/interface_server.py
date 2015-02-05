from Tkinter import *
import tkMessageBox
from multiprocessing import Process
import os
fields = ["Port"]

def fetch(entries):
    TCP_PORT = int(entries[0].get())

    try:
         p = Process(target=os.system, args=("python server.py {}".format(TCP_PORT),))
         p.start()
         root.destroy()
    except Exception, e:
        tkMessageBox.showerror('Error', e.strerror)

def quit(entries):
    root.destroy()


def makeform(root, fields):
    entries = []
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=5, text=field)
        ent = Entry(row)
        row.pack(side=TOP, fill=X)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries.append(ent)
    return entries

root = Tk()
label = Label(root, text="Enter connection data",font="Arial 13")
label.pack(side=TOP,fill=X)
ents = makeform(root, fields)
root.bind("<Return>", (lambda event: fetch(ents)))
Button(root, text="Enter", command = (lambda: fetch(ents))).pack(side=LEFT)
Button(root, text="Quit", command = (lambda: quit(ents))).pack(side=RIGHT)
root.mainloop()
