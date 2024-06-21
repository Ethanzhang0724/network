# coding=utf-8
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import re
from datetime import datetime
import time
from PIL import Image,ImageTk
import generalVar
from netaddr import *
import getMac
import getMac1
import threading
from queue import Queue


class MainWindow():
    def __init__(self):
        self.dic=''
        self.win=Toplevel()
        self.win.title("Search Mac Address")
        self.win.resizable(0, 0)
        #self.win.config(bg='white')
        x = (self.win.winfo_screenwidth() - 800) / 2
        y = (self.win.winfo_screenheight() - 600) / 2
        self.win.geometry('800x600+%d+%d' % (x, y))
        Label(self.win,text="Switch IOS:", relief='groove',anchor="w").place(x=30,y=10,width=120,height=30)
        Label(self.win, text="Site Name ：", relief='groove', anchor="w").place(x=30, y=120, width=120, height=30)
        Label(self.win, text="The MAC You want to Search", relief='groove', anchor="w").place(x=250, y=10, width=180, height=30)
        Label(self.win, text="The IP You want to Search", relief='groove', anchor="w").place(x=250, y=290, width=180,height=30)
        Label(self.win, text="Result", relief='groove', anchor="w").place(x=500, y=10, width=250, height=30)
        img1 = Image.open("../health/picture/arrow.jpg")
        img = ImageTk.PhotoImage(img1)
        arrowlabel=Label(self.win,image=img)
        arrowlabel.place(x=440,y=230,width=59,height=58)
        arrowlabel.bind("<Button-1>",self.getdomainuser)

        self.val=StringVar()
        self.val.set('cisco_ios')
        ios_items=("cisco_ios","cisco_asa", "cisco_ftd", "cisco_nxos", "cisco_s300", "cisco_tp", "cisco_wlc", 'cisco_xe',
                   'cisco_xr','checkpoint_gaia')
        ios_cb=Combobox(self.win,values=ios_items,textvariable=self.val)
        ios_cb.place(x=30,y=60,width=120,height=30)
        self.val2 = StringVar()
        self.val2.set('YZ Campus')
        self.site_items=("YZ Campus",'YZ Prd',"SZ Campus","SZ Prd","Shanghai Office",'JZ Campus','Subang')
        self.site_ips=("10.130.192.2","10.130.211.2",'10.130.213.2','10.130.203.2','10.130.148.2','10.130.204.2','10.130.220.2')
        site_cb = Combobox(self.win, values=self.site_items, textvariable=self.val2)
        site_cb.place(x=30, y=160, width=120, height=30)
        scr2 = Scrollbar(self.win)
        scr1 = Scrollbar(self.win)
        scr3=Scrollbar(self.win)
        scr1.place(x=430,y=60,width=10,height=200)
        scr2.place(x=750, y=60, width=10, height=450)
        scr3.place(x=430, y=330, width=10, height=200)
        self.text1 = Text(self.win, undo=True, autoseparator=True, yscrollcommand=scr1.set)
        self.text1.place(x=250, y=60, width=180, height=200)
        self.text2 = Text(self.win, undo=True, autoseparator=True,yscrollcommand=scr2.set)
        self.text2.place(x=500, y=60, width=250, height=450)
        self.text3 = Text(self.win, undo=True, autoseparator=True, yscrollcommand=scr3.set)
        self.text3.place(x=250, y=330, width=180, height=200)
        Button(self.win, text="START",command=self.getdomainuser).place(x=500, y=520, width=120, height=40)
        scr1.config(command=self.text1.yview)
        scr2.config(command=self.text2.yview)
        self.win.mainloop()


    def getdomainuser(self,*event):
        str_mac = self.text1.get(0.0, END).strip()
        str_ip = self.text3.get(0.0, END).strip()
        str_macs=[i.strip() for i in str_mac.splitlines()]
        self.ips=[i.strip() for i in str_ip.splitlines()]
        self.macs=[]
        try:
            if len(str_mac)>0:
               for i in str_macs:
                   mac = EUI(i)
                   mac.dialect = mac_cisco
                   self.macs.append(mac)
               self.index = self.site_items.index(self.val2.get())
               self.ip = self.site_ips[self.index]
               print(self.ip)
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
               self.entryenable.bind('<Return>', self.last)
               self.entryenable.place(x=110, y=80, width=141, height=21)
               self.entrypwd.bind('<Return>', self.last)
               Button(self.root, text='RUN', command=self.last).place(x=150, y=120)
               self.root.mainloop()
            elif len(str_ip)>0 and len(str_mac)==0:
                self.macs=self.ips
                self.index = self.site_items.index(self.val2.get())
                self.ip = self.site_ips[self.index]
                print(self.ip)
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
                self.entryenable.bind('<Return>', self.last)
                self.entryenable.place(x=110, y=80, width=141, height=21)
                self.entrypwd.bind('<Return>', self.last)
                Button(self.root, text='RUN', command=self.last).place(x=150, y=120)
                self.root.mainloop()
            else:
                showerror('错误', '请输入 ip或者MAC ')
        except:
            showerror('错误','请检查 '+str_mac+' 格式')
            return
    def last(self,*event):
        if self.entryuser.get()!='' and self.entrypwd.get()!='':

            username = self.entryuser.get()
            password = self.entrypwd.get()
            secret = self.entryenable.get()
            ios = self.val.get()
            threads=[]
            if self.index in [1,3]:
                for mac in self.macs:
                    t = threading.Thread(target=getMac1.run,
                                         args=(username, password, self.ip, str(mac), secret, ios,Queue()))
                    t.start()
                    threads.append(t)
                for t in threads:
                    t.join()
                #getMac1.run(username, password, self.ip, str(self.mac), secret, ios)    #NEXUS
            else:
                for mac in self.macs:
                    t = threading.Thread(target=getMac.run,
                                         args=(username, password, self.ip, str(mac), secret, ios,Queue()))
                    t.start()
                    threads.append(t)
                for t in threads:
                    t.join()
                #getMac.run(username, password, self.ip, str(self.mac), secret, ios)
            self.root.destroy()
            self.text2.delete(0.0, END)
            for i in generalVar.mac_text:
                self.text2.insert(INSERT, i + '\n')
            generalVar.mac_text=[]
            if self.text1.get(0.0, END).strip() =='':
                for i in generalVar.mac_text1:
                    self.text1.insert(INSERT, i + '\n')
                generalVar.mac_text1=[]
            else:
                self.text3.delete(0.0, END)
        else:
            showwarning('警告', '请输入正确的账号和密码！')
#MainWindow()