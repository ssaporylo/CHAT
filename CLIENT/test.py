# from Tkinter import *
# root =Tk()
# frame = Frame(root)
# user_field = Text(frame, width=15, height=20,background='#3399ff', font="Arial 11")
# text = Text(frame,width=60,height= 20,insertwidth=0,background='gray',font="Arial 11")
# scrl = Scrollbar(frame, command=text.yview)
# text.config(yscrollcommand=scrl.set)
# user_field.pack(side=LEFT)
# text.pack(side=LEFT, expand=True, fill=X)
# scrl.pack(side=LEFT,fill=Y)
# frame.pack(side=TOP, fill=X, expand =True)
# root.mainloop()
# for i in range(70):
#              self.text.insert(END, str(i)+'\n')
from datetime import *
d = datetime.now()
print d.date()