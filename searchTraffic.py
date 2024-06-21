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
import iftraffic
import pandas as pd

class MainWindow():
    def __init__(self):
        self.dic=''
        self.win=Toplevel()
        self.win.title("交换机接口流量")
        self.win.resizable(0, 0)
        #self.win.config(bg='white')
        x = (self.win.winfo_screenwidth() - 800) / 2
        y = (self.win.winfo_screenheight() - 600) / 2
        self.win.geometry('800x600+%d+%d' % (x, y))
        Label(self.win,text="选择网络设备IOS:", relief='groove',anchor="w").place(x=30,y=10,width=120,height=30)
        Label(self.win, text="选择或创建文件夹以保存结果：", relief='groove', anchor="w").place(x=30, y=120, width=200, height=30)
        Label(self.win, text="输入网络设备IP地址：", relief='groove', anchor="w").place(x=250, y=10, width=180, height=30)
        Label(self.win, text="Result:", relief='groove', anchor="w").place(x=500, y=10, width=250, height=30)
        img1 = Image.open("../health/picture/arrow.jpg")
        img = ImageTk.PhotoImage(img1)
        arrowlabel=Label(self.win,image=img)
        arrowlabel.place(x=440,y=230,width=59,height=58)
        arrowlabel.bind("<Button-1>",self.getdomainuser)
        self.filelabel=Label(self.win, text='文件夹路径：\n', wraplength=200)
        self.filelabel.place(x=30, y=200)
        self.val=StringVar()
        self.val.set('cisco_ios')
        ios_items=("cisco_ios","cisco_asa", "cisco_ftd", "cisco_nxos", "cisco_s300", "cisco_tp", "cisco_wlc", 'cisco_xe',
                   'cisco_xr','checkpoint_gaia')
        ios_cb=Combobox(self.win,values=ios_items,textvariable=self.val)
        ios_cb.place(x=30,y=60,width=120,height=30)
        Button(self.win, text="选择txt文件",command=self.getip).place(x=250, y=60, width=100, height=30)
        Button(self.win, text="选择文件夹", command=self.getdic).place(x=30, y=160, width=100, height=30)
        #Label(self.win, text="或者手动添加IP:", relief='groove', anchor="center").place(x=250, y=110, width=100, height=30)
        #scr1=Scrollbar(self.win)
        scr2 = Scrollbar(self.win)
        scr1 = Scrollbar(self.win)
        scr1.place(x=430,y=110,width=10,height=400)
        scr2.place(x=750, y=60, width=10, height=450)
        self.text1 = Text(self.win, undo=True, autoseparator=True, yscrollcommand=scr1.set)
        self.text1.place(x=250, y=110, width=180, height=400)
        self.text1.insert(INSERT, '(可在下方手动添加IP:)\n')
        self.text2 = Text(self.win, undo=True, autoseparator=True,yscrollcommand=scr2.set)
        self.text2.place(x=500, y=60, width=250, height=450)
        Button(self.win, text="START",command=self.getdomainuser).place(x=500, y=520, width=120, height=40)
        scr1.config(command=self.text1.yview)
        scr2.config(command=self.text2.yview)
        self.win.mainloop()
    def getip(self):
        a=[]
        file1=askopenfilenames(title="选择文件",filetype=[("txt文件","*.txt")])
        for i in file1:
            with open(i,'r') as f:
                for ii in f.readlines():
                    if ii!='' and ii!='\n' and ii!='\t':
                        a.append(ii.strip())
        for i in a:
            self.text1.insert(INSERT,i+'\n')
    def getdic(self):
        self.dic=askdirectory(title='选择或创建一个文件夹',initialdir=pathlib.Path.cwd().drive+'\\')
        #Label(self.win,text='文件夹路径：\n'+self.dic, wraplength=200).place(x=30,y=200)
        self.filelabel.config(text='文件夹路径：\n'+self.dic)
    def getdomainuser(self,*event):
        self.ips=[]
        str_ip=self.text1.get(0.0,END)
        for stp,i in enumerate(str_ip.splitlines()):
            result=re.search(r"^\s*((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\s*$", i)
            result1=re.search(r".*添加.*", i)
            if result != None:
                self.ips.append(result.group().strip())
            elif result1 == None and i.strip() != '':
                showerror('错误提示','第'+str(stp+1)+'行的IP格式不正确\n\n'+i)
                return False

        if len(self.ips)>0 :
            self.root = Toplevel()
            x = (self.root.winfo_screenwidth() - 307) / 2
            y = (self.root.winfo_screenheight() - 200) / 2
            self.root.geometry('307x200+%d+%d' % (x, y))
            self.root.title('域账号信息')
            Label(self.root, text="账号 ").place(x=75, y=20, width=61, height=21)
            Label(self.root, text="密码 ").place(x=75, y=50, width=61, height=21)
            Label(self.root, text="Enable密码(可选) ").place(x=5, y=80, width=100, height=21)
            self.entryuser = Entry(self.root)
            self.entryuser.place(x=110, y=20, width=141, height=21)
            self.entrypwd = Entry(self.root, show='*')
            self.entrypwd.place(x=110, y=50, width=141, height=21)
            self.entryenable = Entry(self.root, show='*')
            self.entryenable.bind('<Return>',self.last)
            self.entryenable.place(x=110, y=80, width=141, height=21)
            self.entrypwd.bind('<Return>',self.last)
            Button(self.root, text='开始执行', command=self.last).place(x=150, y=120)
            self.root.mainloop()
        else:
            showerror("错误", '请检查IP地址是否正确')
    def last(self,*event):
        if self.entryuser.get()!='' and self.entrypwd.get()!='':
            now = datetime.now()
            threads = []
            username = self.entryuser.get()
            password = self.entrypwd.get()
            date = '%s-%s-%s' % (now.year, now.month, now.day)  ## 赋值
            commands = ['end','show interfaces summary']
            secret = self.entryenable.get()
            ios = self.val.get()
            if self.dic!='':
                f1 = open(self.dic + "\\" + date + "_failed_interface.txt", 'a+')
                dic1=self.dic
                #f = open(self.dic + "\\" + date + "_interfaces.txt", 'a+')
                #f=pd.ExcelWriter(self.dic + "\\" + date + "_interfaces.xlsx")
                for ip in self.ips:
                    t = threading.Thread(target=iftraffic.if_ssh,
                                         args=(username, password, ip, commands, secret, date, dic1, f1, Queue(), ios))
                    t.start()
                    threads.append(t)
                for t in threads:
                    t.join()
                #    iftraffic.if_ssh(username, password, ip, commands, secret, f, f1, ios)
                f1.close()
                self.text2.delete(0.0, END)
                self.text2.insert(INSERT, generalVar.interface_text)
                self.root.destroy()

            else:
                for ip in self.ips:
                    t = threading.Thread(target=iftraffic.if_ssh1,
                                         args=(username, password, ip, commands, secret, Queue(), ios))
                    t.start()
                    threads.append(t)
                for t in threads:
                    t.join()
                if len(generalVar.failed_interface)>0:
                    showerror('未成功获取的设备：',generalVar.failed_interface)
                    generalVar.failed_interface=[]
                self.text2.delete(0.0, END)
                self.text2.insert(INSERT, generalVar.interface_text)
                self.root.destroy()

        else:
            showwarning('警告', '请输入正确的账号和密码！')
#MainWindow()