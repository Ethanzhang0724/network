#coding=utf-8
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import re
import pathlib
from datetime import datetime
import time
from PIL import Image,ImageTk
from netaddr import *


class MainWindow():
    def __init__(self):
        self.dic=''
        self.win=Toplevel()
        self.win.title("mac查询工具")
        self.win.resizable(0, 0)
        x = (self.win.winfo_screenwidth() - 590) / 2
        y = (self.win.winfo_screenheight() - 600) / 2
        self.win.geometry('590x600+%d+%d' % (x, y))
        Label(self.win, text="添加要查询的MAC地址：", relief='groove', anchor="w").place(x=20, y=10, width=200, height=30)
        Label(self.win, text="mac归属信息", relief='groove', anchor="w").place(x=290, y=10, width=250, height=30)
        Label(self.win, text="mac地址格式转换", relief='groove', anchor="w").place(x=290, y=280, width=250, height=30)
        img1 = Image.open("../health/picture/arrow.jpg")
        img = ImageTk.PhotoImage(img1)
        arrowlabel=Label(self.win,image=img)
        arrowlabel.place(x=230,y=230,width=59,height=58)
        arrowlabel.bind('<Button-1>',self.getlast)
        scr2 = Scrollbar(self.win)
        scr1 = Scrollbar(self.win)
        scr3 = Scrollbar(self.win)
        scr1.place(x=220,y=60,width=10,height=200)
        scr2.place(x=540, y=60, width=10, height=200)
        scr3.place(x=540, y=320, width=10, height=200)
        self.text1 = Text(self.win, undo=True, autoseparator=True, yscrollcommand=scr1.set)
        self.text1.place(x=20, y=60,width=200, height=200)
        self.text2 = Text(self.win, undo=True, autoseparator=True, yscrollcommand=scr2.set)
        self.text2.place(x=290, y=60, width=250, height=200)
        self.text3 = Text(self.win, undo=True, autoseparator=True, yscrollcommand=scr3.set)
        self.text3.place(x=290, y=320, width=250, height=200)
        Button(self.win, text="查看",command=self.getlast).place(x=290, y=540, width=120, height=40)
        scr1.config(command=self.text1.yview)
        scr2.config(command=self.text2.yview)
        self.win.mainloop()

    def getlast(self,*event):
        self.macs=[]
        str_mac=self.text1.get(0.0, END)
        for i in str_mac.splitlines():
            self.macs.append(i.strip())
        if len(self.macs)>0:
            self.text2.delete(0.0, END)
            self.text3.delete(0.0, END)
            for i in self.macs:
                try:
                    mac = EUI(i)
                    self.text2.insert(INSERT, mac.info)
                    self.text2.insert(INSERT, '\n')
                    mac.dialect = mac_cisco
                    self.text3.insert(INSERT, 'Cisco Format: ')
                    self.text3.insert(INSERT, mac)
                    self.text3.insert(INSERT, '\n')
                    mac.dialect = mac_unix
                    self.text3.insert(INSERT, 'Unix Format: ')
                    self.text3.insert(INSERT, mac)
                    self.text3.insert(INSERT, '\n')
                    mac.dialect = mac_eui48
                    self.text3.insert(INSERT, 'EUI48 Format: ')
                    self.text3.insert(INSERT, mac)
                    self.text3.insert(INSERT, '\n')
                    mac.dialect = mac_bare
                    self.text3.insert(INSERT, 'Bare Format: ')
                    self.text3.insert(INSERT, mac)
                    self.text3.insert(INSERT, '\n')
                except:
                    showerror('错误','无法查找到MAC '+i+' 信息')


        else:
            showerror("错误", '请填写正确mac地址')

#MainWindow()