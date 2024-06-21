from tkinter import *
from tkinter.ttk import *
from PIL import Image,ImageTk
import datetime
import service
import sys
import exec
import save
import searchSN
import searchSubnet
import checkMAC
import user
import searchOnline
import searchVlsm
import searchMac
import searchTraffic
import searchport

class MainWindow():

    def __init__(self):
        self.win=Tk()
        self.win.title("Pirelli Network Management SYSTEM")
        self.win.resizable(0, 0)
        x = (self.win.winfo_screenwidth() - 997) / 2
        y = (self.win.winfo_screenheight() - 580) / 2
        self.win.geometry('997x561+%d+%d' % (x, y))
        img1 = Image.open("picture/main2.JPG")
        img = ImageTk.PhotoImage(img1)
        Label(self.win,image=img).place(x=0, y=0, width=997, height=561)
        self.menuMain=Menu()
        self.menu4 = Menu(self.menuMain, tearoff=False)
        self.menu6 = Menu(self.menuMain, tearoff=False)
        self.menu4.add_command(label='OnlineDevice', command=searchOnline.MainWindow)
        self.menu4.add_command(label='BroadcastInfor', command=searchSubnet.MainWindow)
        self.menu4.add_command(label='VLSM', command=searchVlsm.MainWindow)
        self.menuMain.add_command(label="ExcuteCommands", command=exec.MainWindow)
        self.menuMain.add_command(label="SaveConfig", command=save.MainWindow)
        self.menuMain.add_command(label="SearchSerialNumber", command=searchSN.MainWindow)
        self.menuMain.add_command(label="SearchEndMAC", command=searchMac.MainWindow)
        self.menuMain.add_command(label="TrafficAnalystics", command=searchTraffic.MainWindow)
        self.menuMain.add_cascade(label="SubnetsInfor",menu=self.menu4 )
        self.menuMain.add_command(label="TransformMacFormat", command=checkMAC.MainWindow)
        self.menuMain.add_command(label="PortScan", command=searchport.MainWindow)
        self.menu6.add_command(label="UserManagement",command=user.MainWindow)
        self.menu6.add_command(label="EXIT", command=self.win.destroy)
        self.menuMain.add_cascade(label="System", menu=self.menu6)

        self.labelInfo = Label(self.win,
                              text="  CurrentUser：" + service.username + " | Time：" + datetime.datetime.now().strftime(
                                  '%Y-%m-%d %H:%M:%S') + "  | Copyright：Zhang Yixing")
        self.labelInfo.place(x=0, y=537, width=997, height=24)

        self.win.config(menu=self.menuMain)
        self.win.after(1000, self.timeUpdate)
        self.win.mainloop()


    def timeUpdate(self):
        global labelInfo
        self.time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.labelInfo.config(text="  CurrentUser：" + service.username + " | Time：" + datetime.datetime.now().strftime(
                                  '%Y-%m-%d %H:%M:%S') + "  | Copyright：Zhang Yixing")
        self.win.after(100, self.timeUpdate)   # 每隔一秒，时间变化一次

#MainWindow()