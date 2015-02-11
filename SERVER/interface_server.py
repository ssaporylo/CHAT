from Tkinter import *
import tkMessageBox
from multiprocessing import Process
import os
import thread
import socket

fields = ["Port"]

class Create_interface(object):
    def __init__(self, field, root):
        self.root =root
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.label = Label(self.root, text="Enter connection data",font="Arial 13")
        self.label.pack(side=TOP,fill=X)
        self.entries = self.makeform(field)
        self.enter = Button(self.root, text="Enter", command=self.fetch)
        self.enter.pack(side=LEFT)
        self.close = Button(self.root, text="Quit", command = self.quit).pack(side=RIGHT)
        self.processes = []

    def makeform(self,fields):
        entries = []
        for field in fields:
            row = Frame(self.root)
            lab = Label(row, width=5, text=field)
            ent = Entry(row)
            row.pack(side=TOP, fill=X)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)
            entries.append(ent)
        return entries

    def fetch(self):
        try:
            TCP_PORT = int(self.entries[0].get())
            s=socket.socket()
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
            s.bind(("localhost", TCP_PORT))
            global p
            p = Process(target=os.system, args=("python server.py {}".format(TCP_PORT),))
            p.start()
            self.processes.append(p.pid)
            tkMessageBox.showinfo('Running', 'Server started on port {}'.format(TCP_PORT))

        except Exception, e:
            tkMessageBox.showerror('Error', e)

    def quit(self):
        for p in self.processes:
            print p
            thread.start_new_thread(os.kill,(p,9))
        root.destroy()

root = Tk()
Create_interface(fields, root)
root.mainloop()
