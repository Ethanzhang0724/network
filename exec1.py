# coding=utf-8
import threading
import time
import netmiko
import paramiko
from queue import Queue
import socket
from getpass import getpass
import re
from datetime import datetime
import telnetlib
import os
from pathlib import Path
from netaddr import *
from pythonping import *
import sys
import asyncio
from ciscoconfparse import CiscoConfParse

class CiscoDevice(threading.Thread):
    def __init__(self, username, password, ip, date, commands, secret, f1, dic, ios='cisco_ios'):
        threading.Thread.__init__(self)
        # super(CiscoDevice,self).__init__(username,password,ip,date,commands,f1)
        self.username = username
        self.password = password
        self.date = date
        self.commands = commands
        self.ip = ip
        self.f1 = f1
        self.secret = secret
        self.ios = ios
        self.dic = dic
    def run(self):
        self.sshsession()

    def sshsession(self):
        try:
            sw = {'device_type': self.ios , 'ip': self.ip, 'username': self.username,
                  'password': self.password, 'secret': self.secret}
            connect = netmiko.ConnectHandler(**sw)  ## 字典赋值用** , 列表用*
            connect.enable()
            output = connect.send_config_set(self.commands)
            print(output)
            with open(self.dic + "\\"+ self.date + ' ' + self.ip + '.txt', 'w+') as f:
                f.write(output)
        except netmiko.ssh_exception.NetmikoAuthenticationException:
            print('未知异常 ' + self.ip+'\n')
            self.f1.write(self.ip + '\n')
        except netmiko.ssh_exception.NetmikoTimeoutException:
            print('unreachable ip,will try with telnet: ' + self.ip+'\n')
            self.telnetsession()
            #self.f1.write(self.ip + '\n')
        except socket.error:
            print('file Path not found: ' + self.ip+'\n')
            self.f1.write(self.ip + '\n')
        except netmiko.NetMikoAuthenticationException:
            print("1:    " + self.ip+'\n')
            self.f1.write(self.ip + '\n')
        except netmiko.ssh_exception.AuthenticationException:
            print('密码错误或者未启用tacas导致登录失败:     ' + self.ip+'\n')
            self.f1.write(self.ip + '\n')
        except paramiko.ssh_exception.SSHException:
            print('SSH Unenabled,try to login with Telnet:  ' + self.ip+'\n')
            self.telnetsession()
            # self.f1.write(self.ip + '\n')
        except netmiko.ssh_exception.SSHException:
            print('4:   ' + self.ip+'\n')
            self.f1.write(self.ip + '\n')
        except netmiko.ssh_autodetect:
            print('5:   ' + self.ip+'\n')
            self.f1.write(self.ip + '\n')
        except Exception:
            print('6:   ' + self.ip+'\n')
            self.f1.write(self.ip + '\n')
        except:
            print('7:    ' + self.ip+'\n')
            self.f1.write(self.ip + '\n')

    def to_bytes(line):
        return f"{line}\n".encode("utf-8")

    def telnetsession(self):
        try:
            tn = telnetlib.Telnet(self.ip)
            print('Telenet sucessfully:   ' + self.ip)
            #tn.expect(b"[r'[Uu]sername: ']")
            tn.read_until(b"Username: ")               #2960x
            tn.write(self.username.encode('ascii') + b'\n')
            tn.read_until(b"Password: ")

            tn.write(self.password.encode('ascii') + b'\n')
            #tn.read_until(b"\s*>")
            #tn.write(self.secret.encode('ascii') + b'\n')
            tn.write(b'terminal length 0\n')
            tn.write(b'conf t\n')
            for command in self.commands:
                tn.write(command.encode('ascii') + b'\n')
                time.sleep(0.5)
            tn.write(b'end\n')
            #tn.write(b'exit\n')
            tn.write(b'exit\n')
            # output=tn.read_very_eager().decode('ascii')
            output = tn.read_all().decode('ascii')
            print(output)
            with open(self.dic + "\\"+self.date + ' ' + self.ip + '.txt', 'w+') as f:
                f.write(output)
            tn.close()
        except IOError:
            print('Also telnet unsucessfully:   ' + self.ip)
            self.f1.write(self.ip + '\n')
        except Exception:
            print('t1  '+self.ip+'\n')
            self.f1.write(self.ip + '\n')
        except:
            print('t2 '+self.ip+'\n')
            self.f1.write(self.ip + '\n')

    def enablesshv2(self):
        try:
            tn1 = telnetlib.Telnet(self.ip)
            print('自动为%s尝试启用SSHV2:   ' % (self.ip))
            tn1.read_until(b"Username: ")
            tn1.write(self.username.encode('ascii') + b'\n')
            tn1.read_until(b"Password: ")
            tn1.write(self.password.encode('ascii') + b'\n')
            tn1.write(b'terminal length 0\n')
            tn1.write(b'conf t\n')
            tn1.write(b'ip domain name pirelli.com\n')
            tn1.write(b'crypto key generate rsa general-keys\n')
            if tn1.read_until(b"% Do you really want to replace them? [yes/no]: "):
                tn1.write(b'yes\n')
            time.sleep(0.5)
            tn1.write(b'\n')
            tn1.write(b'\n')
            tn1.write(b'crypto key generate rsa general-keys modulus 1024\n')
            time.sleep(1)
            tn1.write(b'ip ssh version 2\n')
            tn1.write(b'line vty 0 15\n')
            tn1.write(b'transport input all\n')
            tn1.write(b'end\n')
            tn1.write(b'exit\n')
            output1 = tn1.read_all().decode('ascii')
            print(output1)
            tn1.close()
        except IOError:
            print('启用失败1')
        except Exception:
            print('启用失败2')
        except:
            print('启用失败3')

'''def module1():
    print('\nInstructions:\n1.you will execute this script and results will be \
saved automatically in %s\\ethon\\option1\n' % Path.cwd())
    print('2.The ip list and commands you input will be saved automatically in %s\\ethon\\option1\n' % Path.cwd())
    if not os.path.exists(os.getcwd() + '\\ethon\\option1'):
        os.makedirs(os.getcwd() + '\\ethon\\option1')
    print("Please input the network devices' ip list (split with Enter ,end with '$') :")
    threads=[]
    endstr = '$'
    ip = ''
    command=''
    ips=[]
    commands=[]
    for line in iter(input, endstr):
        ip += line+'\n'
    print("Please input commands(split with Enter ,end with '$') :")
    for line in iter(input, endstr):
        command += line+'\n'
    for i in ip.splitlines():
        ips.append(i.strip())
    for i in command.splitlines():
        commands.append(i.strip())
    with open('.\\ethon\\option1\\'+date+'_ip.txt', 'w+') as f:
        f.write(ip)
    with open('.\\ethon\\option1\\'+date+'_commands.txt', 'w+') as f:
        f.write(command)
    username = input('Input Login username: ')
    password = input("Input Login password: ")
    ios=input("Device_type (cisco platform(cisco_asa, cisco_ftd, cisco_ios(default), cisco_nxos, cisco_s300, cisco_tp, cisco_wlc, cisco_xe, cisco_xr)\n\
checkpoint platform(checkpoint_gaia) :  ")
    secret = input("Input Enable Password (optional): ")
    print(f"程序于{time.strftime('%X')}开始\n")
    # os.access(os.getcwd(),os.W_OK)
    f1 = open(r".\ethon\option1\fail.txt", 'a+')
    #f1.write('------------程序于 '+date+'  '+time.strftime('%X')+'开始--------------------\n')
    if ios != '':
        for ip in ips:
            # ii = re.findall(r'^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$', ip)
            ii = re.search(
                r"^\s*((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\s*$", ip)
            if ii != None:
                t = CiscoDevice(username, password, ii.group(), date, commands, secret, f1,option, ios.strip())
                t.start()
                threads.append(t)
            else:
                print('无效地址： ' + ip + '\n')
                f1.write(ip + '\n')
        for t in threads:
            t.join()

    else:
        for ip in ips:
            # ii = re.findall(r'^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$', ip)
            ii = re.search(
                r"^\s*((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\s*$", ip)
            if ii != None:
                t = CiscoDevice(username, password, ii.group(), date, commands, secret, f1,option)
                t.start()
                threads.append(t)
            else:
                print('无效地址： ' + ip + '\n')
                f1.write(ip + '\n')
        for t in threads:
            t.join()
        # f1.write('------------程序于 '+date+'  '+time.strftime('%X')+'结束--------------------\n')
    f1.close()
    print(f"程序于{time.strftime('%X')}结束")   '''







