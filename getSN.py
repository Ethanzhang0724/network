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
from ciscoconfparse import CiscoConfParse
import generalVar


def sn_ssh(username, password, ip, commands, secret,f, f1 , queue2, ios='cisco_ios'):
    try:
        sw = {'device_type': ios, 'ip': ip, 'username': username, 'password': password, 'secret': secret}
        connect = netmiko.ConnectHandler(**sw)  ## 字典赋值用** , 列表用*
        #connect=netmiko.ConnLogOnly(**sw)
        connect.enable()
        output = connect.send_config_set(commands)
        cfg = output.splitlines()
        parse = CiscoConfParse(cfg)
        obj=''
        for obj in parse.find_objects(
                r"[sS][yY][sS][tT][eE][mM]\s*[Ss][eE][rR][iI][aA][lL]\s*[nN][uU][mM][bB][eE][rR]"):
            if len(obj.ioscfg)>0:
                for i1 in obj.ioscfg:
                    i2=re.search(r":.*",i1)
                    i=i2.group()
                    generalVar.sn_text.append(ip + i)
                    f.write(ip + i + '\n')

        if obj == '':
            f1.write('未获取有效信息: ' + ip + '\n')
    except netmiko.ssh_exception.NetmikoAuthenticationException:
        print('未知异常 ' + ip + '\n')
        f1.write(ip + '\n')
    except netmiko.ssh_exception.NetmikoTimeoutException:
        print('unreachable ip,will try telnet:   ' + ip + '\n')
        sn_telnet(username, password, ip, commands, f, f1)
        # f1.write(ip + '\n')
    except socket.error:
        print('file Path not found: ' + ip + '\n')
        f1.write(ip + '\n')
    except netmiko.NetMikoAuthenticationException:
        print("1:    " + ip + '\n')
        f1.write(ip + '\n')
    except netmiko.ssh_exception.AuthenticationException:
        print('密码错误或者未启用tacas导致登录失败:     ' + ip + '\n')
        f1.write(ip + '\n')
    except paramiko.ssh_exception.SSHException:
        print('SSH Unenabled,try to login with Telnet:  ' + ip + '\n')
        sn_telnet(username, password, ip, commands, f, f1)
        # self.f1.write(self.ip + '\n')
    except netmiko.ssh_exception.SSHException:
        print('4:   ' + ip + '\n')
        f1.write(ip + '\n')
    except netmiko.ssh_autodetect:
        print('5:   ' + ip + '\n')
        f1.write(ip + '\n')
    except Exception:
        print('6:   ' + ip + '\n')
        f1.write(ip + '\n')
    except:
        print('7:    ' + ip + '\n')
        f1.write(ip + '\n')


def sn_telnet(username, password, ip, commands,f, f1):
    try:
        tn = telnetlib.Telnet(ip)
        print('Telenet sucessfully:   ' + ip)
        tn.read_until(b"Username: ")
        tn.write(username.encode('ascii') + b'\n')
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b'\n')
        tn.write(b'terminal length 0\n')
        tn.write(b'conf t\n')
        for command in commands:
            tn.write(command.encode('ascii') + b'\n')
        time.sleep(0.5)
        tn.write(b'end\n')
        tn.write(b'exit\n')
        # output=tn.read_very_eager().decode('ascii')
        # print(output)
        output = tn.read_all().decode('ascii')
        cfg = output.splitlines()
        parse = CiscoConfParse(cfg)
        for obj in parse.find_objects(
                    r"[sS][yY][sS][tT][eE][mM] [Ss][eE][rR][iI][aA][lL] [NN][uU][mM][bB][eE][rR]"):
            if obj.ioscfg!=[]:
                for i in obj.ioscfg:
                    print(ip + " : " + i + '\n')
                    f.write(ip + " : " + i + '\n')
                    generalVar.sn_text.append(ip + " : " + i)
            else:
                f1.write('未获取有效信息: '+ip+'\n')
        tn.close()
    except IOError:
        print('Also telnet unsucessfully:   ' + ip+'\n')
        f1.write(ip + '\n')
    except Exception:
        print('t1 '+ip+'\n')
        f1.write(ip + '\n')
    except:
        print('t2 '+ip+'\n')
        f1.write(ip + '\n')