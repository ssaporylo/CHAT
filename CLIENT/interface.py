from Tkinter import *
import socket
import thread
import pickle

with open('conf.pickle', 'rb') as handle:
  config = pickle.load(handle)

def _send_request(message):
    TCP_IP = config["IP_ADRESS"]
    TCP_PORT = config["PORT"]
    BUFFER_SIZE = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(message)
    data = s.recv(BUFFER_SIZE)
    s.close()


class Create_title(object):
    def __init__(self,root):
        self.frame = Frame(root)
        self.label1 = Label(self.frame, text="Users",anchor='w', width = 15, font="times 14")
        self.label2 = Label(self.frame, text="Messages", width = 40, font="times 14")
        self.label1.pack(side=LEFT)
        self.label2.pack(side=RIGHT, expand=YES, fill=X)
        self.frame.pack(side=TOP, fill=X)

class Create_chat_fields(object):
    def __init__(self,root):
        self.frame = Frame(root)
        self.user_field = Text(self.frame, width=15, height=20,background='#3399ff', font="times 11")
        self.scrl_user = Scrollbar(self.frame, command=self.user_field.yview)
        self.user_field.config(yscrollcommand=self.scrl_user.set)
        self.text = Text(self.frame,width=60,height= 20,insertwidth=0,background='gray',font="times 11")
        self.scrl = Scrollbar(self.frame, command=self.text.yview)
        self.write_history(self.text, self.scrl)
        self.text.config(yscrollcommand=self.scrl.set)
        self.text.tag_config('text', font=('times', 11, 'underline'))
        self.text.tag_config('status', font=('times', 11, 'bold'))
        self.user_field.pack(side=LEFT)
        self.scrl_user.pack(side=LEFT,fill=Y)
        self.text.pack(side=LEFT, expand=True, fill=X)
        self.scrl.pack(side=LEFT,fill=Y)
        self.frame.pack(side=TOP, fill=X, expand =True)
        self.frame.pack(side=TOP, fill=X, expand =True)
        events = ["<BackSpace>","<Delete>","<Control-x>","<Button-1>"]
        for i in events:
            self.text.bind(i,self.unbindevent)
            self.user_field.bind(i,self.unbindevent)

    def write_history(self, text, scrl):
        f = open('archive.txt', 'r')
        for message in f.readlines():
            text.insert(INSERT,message)
            insert_row = int(float(text.index("end")))-2
            try:
                start = "{0}.{1}".format(str(insert_row),message.index('<'))
                end = "{0}.{1}".format(str(insert_row),message.index('>')+1)
                text.tag_add('text', start, end)
            except ValueError, e:
                start = "{0}.0".format(str(insert_row))
                end = "{0}.{1}".format(str(insert_row),len(message))
                text.tag_add('status', start, end)

    def unbindevent(self, event):
        return 'break'


class Create_form(object):
    def __init__(self, root, tex):
        self.tex = tex
        self.row = Frame(root)
        self.clear = Button(self.row, height=3, text="Clear history", command= self.clear_history)
        self.lab = Button(self.row, height=3, text="Send", command= self.fetch)
        self.ent = Text(self.row,background='#e7e037', height = 3)
        self.row.pack(side=TOP, fill=X)

        self.ent.bind('<Return>', self.unbindevent)
        self.ent.bind('<Return>', self.fetch)
        self.ent.pack(side=LEFT, expand=YES, fill=X)
        self.lab.pack(side=LEFT)
        self.clear.pack(side=RIGHT)


    def fetch(self,event=False):

        data =''.join([i for i in self.ent.get('1.0', END).split('\n') if i.strip !=''])
        message = 'MESSAGE@<{0}> {1}'.format(config["USER"],data)
        self.ent.delete("1.0", END)
        self.ent.focus_set()
        self.lab.focus_set()
        self.ent.focus_set()
        _send_request(message)

    def unbindevent(self, event):
        return 'break'

    def clear_history(self):
        open("archive.txt","w").close()
        self.tex.text.delete("1.0", END)


def handler_exit():
    thread.start_new_thread(_send_request,('DELETE@{0}'.format(config["USER"]),))
    root.destroy()

def start():
    global root
    root = Tk()
    root.wm_title("CHAT")
    lab = Create_title(root)
    global tex
    tex = Create_chat_fields(root)
    form = Create_form(root,tex)
    root.protocol("WM_DELETE_WINDOW", handler_exit)
    root.mainloop()





