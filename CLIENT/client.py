from Tkinter import *
import socket
import tkMessageBox
import os
import pickle
from multiprocessing import Process

fields = "Host", "Port", "Name"

def fetch(entries):
    TCP_IP = entries[0].get()
    TCP_PORT = int(entries[1].get())
    USER = entries[2].get()
    BUFFER_SIZE = 1024
    message = "REGISTER@{}".format(USER)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(message)
        data = s.recv(BUFFER_SIZE)
        if data.strip() == "User exists":
            tkMessageBox.showwarning('Error', data)
            return
        s.close()
        a = {'USER': USER ,'IP_ADRESS': TCP_IP,"PORT": TCP_PORT}
        with open('conf.pickle', 'wb') as handle:
            pickle.dump(a, handle)
        p = Process(target=os.system, args=("python reader.py",))
        p.start()
        root.destroy()
    except Exception, e:
        print dir(e)
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



