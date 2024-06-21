# coding=utf-8
from tkinter import *
from tkinter.ttk import *
from PIL import Image,ImageTk
import threading
from queue import Queue
import generalVar
import getport
from tkinter.messagebox import *
class MainWindow():
    def __init__(self):
        self.dic=''
        self.win=Toplevel()
        self.win.title("PortScan")
        self.win.resizable(0, 0)
        x = (self.win.winfo_screenwidth() - 590) / 2
        y = (self.win.winfo_screenheight() - 600) / 2
        self.win.geometry('590x600+%d+%d' % (x, y))
        Label(self.win, text="Enter Hostname or Ip address", relief='groove', anchor="w").place(x=20, y=10, width=200, height=30)
        Label(self.win, text="Open Ports", relief='groove', anchor="w").place(x=290, y=10, width=250, height=30)
        Label(self.win, text="Start Port", anchor="w").place(x=20, y=280, width=60,height=20)
        Label(self.win, text="End Port", anchor="w").place(x=110, y=280, width=60, height=20)
        img1 = Image.open("../health/picture/arrow.jpg")
        img = ImageTk.PhotoImage(img1)
        arrowlabel=Label(self.win,image=img)
        arrowlabel.place(x=230,y=230,width=59,height=58)
        arrowlabel.bind('<Button-1>',self.getlast)
        scr2 = Scrollbar(self.win)
        scr1 = Scrollbar(self.win)
        scr1.place(x=220,y=60,width=10,height=200)
        scr2.place(x=540, y=60, width=10, height=450)
        self.text1 = Text(self.win, undo=True, autoseparator=True, yscrollcommand=scr1.set)
        self.text3 = Text(self.win, undo=True, autoseparator=True)
        self.text4 = Text(self.win, undo=True, autoseparator=True)
        self.text1.place(x=20, y=60,width=200, height=200)      #ip address 文本框
        self.text3.place(x=20, y=310, width=60, height=20)      #开始端口
        self.text4.place(x=110, y=310, width=60, height=20)     #结束端口
        self.text2 = Text(self.win, undo=True, autoseparator=True, yscrollcommand=scr2.set)
        self.text2.place(x=290, y=60, width=250, height=450)    #结果文本框
        Button(self.win, text="查看",command=self.getlast).place(x=290, y=520, width=120, height=40)
        scr1.config(command=self.text1.yview)
        scr2.config(command=self.text2.yview)
        self.win.mainloop()

    def getlast(self,*event):
        threads=[]
        startport=int(self.text3.get(0.0,END).strip())
        endport=int(self.text4.get(0.0,END).strip())
        target_host=self.text1.get(0.0,END).strip()
        for port in range(startport,endport+1):
            t = threading.Thread(target=getport.scan_ports, args=(target_host, port, Queue()))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        self.text2.delete(0.0, END)
        for i in generalVar.openports:
            self.text2.insert(INSERT, "开放端口: "+str(i) + '\n')
        showinfo("完成提示",'端口扫描完成')
        generalVar.openports=[]
#MainWindow()

