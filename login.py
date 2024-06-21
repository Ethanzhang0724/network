from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
from tkinter.messagebox import *
import service
import main


class Login():
    def __init__(self):
        self.win=Tk()
        self.win.title("倍耐力网管系统登录")
        #self.win.config(bg='red')
        self.win.resizable(0,0)
        x=(self.win.winfo_screenwidth()-500)/2
        y=(self.win.winfo_screenheight()-300)/2
        self.win.geometry('500x300+%d+%d'% (x,y))
        self.img1=Image.open("picture/3.JPG")
        self.img=ImageTk.PhotoImage(self.img1)
        Label(self.win,image=self.img).place(x=0,y=0,width=500,height=103)
        Label(self.win, text="用户名：").place(x=120, y=140, width=61, height=21)
        self.EntryUser = Entry(self.win)
        self.EntryUser.place(x=193, y=140, width=141, height=20)
        Label(self.win, text="密   码：").place(x=119, y=180, width=61, height=21)  # 密码
        self.EntryPwd = Entry(self.win, show="*")  # 密码文本框
        self.EntryPwd.place(x=192, y=180, width=141, height=20)
        Button(self.win, text="登录", command=lambda: self.openMain('')).place(x=190, y=220, width=61,height=23)  # 登录按钮
        Button(self.win, text="退出", command=self.win.destroy).place(x=270, y=220, width=61, height=23)  # 退出按钮
        self.EntryPwd.bind("<Return>", self.openMain)
        self.win.mainloop()

    def openMain(self, event):
        service.username=self.EntryUser.get()
        pwd=self.EntryPwd.get()
        if self.EntryUser.get() !='' and self.EntryPwd.get() !='':
            result=service.query("select * from tb_user where username= %s and userpwd = %s" ,service.username,pwd)
            if len(result) >0:
                self.win.destroy()
                main.MainWindow()

            else:
                self.EntryUser.delete(0,END)
                self.EntryPwd.delete(0,END)
                showwarning('警告', '请输入正确的用户名和密码！')

        else:
            showerror("错误", "请输入用户名和密码")
            return False

Login()

