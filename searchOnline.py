from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import re
import pathlib
from datetime import datetime
import time
from PIL import Image,ImageTk
import threading
from queue import Queue
import generalVar
from netaddr import *
import getonline

class MainWindow():
    def __init__(self):
        self.dic=''
        self.win=Toplevel()
        self.win.title("查看在线IP")
        self.win.resizable(0, 0)
        x = (self.win.winfo_screenwidth() - 590) / 2
        y = (self.win.winfo_screenheight() - 600) / 2
        self.win.geometry('590x600+%d+%d' % (x, y))
        Label(self.win, text="添加要查询的网段信息：", relief='groove', anchor="w").place(x=20, y=10, width=200, height=30)
        Label(self.win, text="在线IP地址", relief='groove', anchor="w").place(x=290, y=10, width=250, height=30)
        img1 = Image.open("../health/picture/arrow.jpg")
        img = ImageTk.PhotoImage(img1)
        arrowlabel=Label(self.win,image=img)
        arrowlabel.place(x=230,y=230,width=59,height=58)
        arrowlabel.bind('<Button-1>',self.getlast)
        scr2 = Scrollbar(self.win)
        scr1 = Scrollbar(self.win)
        scr1.place(x=220,y=60,width=10,height=400)
        scr2.place(x=540, y=60, width=10, height=450)
        self.text1 = Text(self.win, undo=True, autoseparator=True, yscrollcommand=scr1.set)
        self.text1.place(x=20, y=60,width=200, height=400)
        self.text1.insert(INSERT, '格式如:(192.168.1.0/24)\n')
        self.text2 = Text(self.win, undo=True, autoseparator=True, yscrollcommand=scr2.set)
        self.text2.place(x=290, y=60, width=250, height=450)
        Button(self.win, text="查看",command=self.getlast).place(x=290, y=520, width=120, height=40)
        scr1.config(command=self.text1.yview)
        scr2.config(command=self.text2.yview)
        self.win.mainloop()



    def getlast(self,*event):
        self.ips=[]
        threads=[]
        str_ip=self.text1.get(0.0,END)
        for stp,i in enumerate(str_ip.splitlines()):
            result=re.search(r"^\s*((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/[0-2][0-9]|30\s*$", i)
            result1=re.search(r".*格式.*", i)
            if result != None:
                self.ips.append(result.group().strip())
            elif result1 == None and i.strip() != '':
                showerror('错误提示','第'+str(stp+1)+'行的网段格式不正确\n\n'+i)
                return False

        if len(self.ips)>0 :
            for i in self.ips:
                subnet1 = IPNetwork(i)
                for ip1 in subnet1.iter_hosts():
                    t = threading.Thread(target=getonline.getonline, args=(str(ip1), Queue()))
                    t.start()
                    threads.append(t)
                for t in threads:
                    t.join()
            self.text2.delete(0.0, END)
            for i in generalVar.online_text:
                self.text2.insert(INSERT, "在线: "+i + '\n')
            generalVar.online_text=[]

        else:
            showerror("错误", '请添加网段信息')

#MainWindow()

