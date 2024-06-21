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


def sn_ssh(username, password, ip, commands, secret , queue2, ios='cisco_ios'):
    try:
        sw = {'device_type': ios, 'ip': ip, 'username': username, 'password': password, 'secret': secret}
        connect = netmiko.ConnectHandler(**sw)  ## 字典赋值用** , 列表用*
        #connect = netmiko.ConnLogOnly(**sw)
        connect.enable()
        output = connect.send_config_set(commands)
        if ios=='cisco_ios':
            pattern = r"system\s*serial\s*number\s*:\s*(\S*)"
            result = re.findall(pattern, output, re.I)
            print(result)
            if len(result) == 0:
                generalVar.failed_sn.append(ip)
            else:
                for i in result:
                    generalVar.sn_text.append(ip + ':  ' + i)
        else:
            pattern = r"system\s*serial\s*number\s*:\s*(\S*)|board\s*ID\s*(\S*)"     #可以针对nexus查找,但只能找一个
            result = re.search(pattern, output, re.I)
            if result == None:
                generalVar.failed_sn.append(ip)
            else:
                if result.group(1) != None:
                    generalVar.sn_text.append(ip + ':  ' + result.group(1))
                else:
                    generalVar.sn_text.append(ip + ':  ' + result.group(2))

        '''cfg = output.splitlines()
        parse = CiscoConfParse(cfg)
        obj=''
        for obj in parse.find_objects(
                r"[sS][yY][sS][tT][eE][mM]\s*[Ss][eE][rR][iI][aA][lL]\s*[nN][uU][mM][bB][eE][rR]"):
            if len(obj.ioscfg)>0:
                for i1 in obj.ioscfg:
                    i2 = re.search(r":.*", i1)
                    i = i2.group()
                    generalVar.sn_text.append(ip + i)
        if obj=='':
            generalVar.failed_sn.append(ip) '''
        '''pattern=r"system\s*serial\s*number\s*:\s*(\S*)|board\s*ID\s*(\S*)"
        result=re.search(pattern,output,re.I)
        if result==None:
            generalVar.failed_sn.append(ip)
        else:
            if result.group(1)!=None:
                generalVar.sn_text.append(ip + ':  '+ result.group(1))
            else:
                generalVar.sn_text.append(ip +':  '+ result.group(2))'''

    except netmiko.ssh_exception.NetmikoAuthenticationException:
        print('未知异常 ' + ip + '\n')
        generalVar.failed_sn.append(ip)
    except netmiko.ssh_exception.NetmikoTimeoutException:
        print('unreachable ip,will try telnet:   ' + ip + '\n')
        sn_telnet(username, password, ip, commands)
    except socket.error:
        print('file Path not found: ' + ip + '\n')
        generalVar.failed_sn.append(ip)
    except netmiko.NetMikoAuthenticationException:
        print("1:    " + ip + '\n')
        generalVar.failed_sn.append(ip)
    except netmiko.ssh_exception.AuthenticationException:
        print('密码错误或者未启用tacas导致登录失败:     ' + ip + '\n')
        generalVar.failed_sn.append(ip)
    except paramiko.ssh_exception.SSHException:
        print('SSH Unenabled,try to login with Telnet:  ' + ip + '\n')
        sn_telnet(username, password, ip, commands)
        # self.f1.write(self.ip + '\n')
    except netmiko.ssh_exception.SSHException:
        print('4:   ' + ip + '\n')
        generalVar.failed_sn.append(ip)
    except netmiko.ssh_autodetect:
        print('5:   ' + ip + '\n')
        generalVar.failed_sn.append(ip)
    except Exception:
        print('6:   ' + ip + '\n')
        generalVar.failed_sn.append(ip)
    except:
        print('7:    ' + ip + '\n')
        generalVar.failed_sn.append(ip)

def sn_telnet(username, password, ip, commands):
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
                    r"[sS][yY][sS][tT][eE][mM] [Ss][eE][rR][iI][aA][lL] [Nn][uU][mM][bB][eE][rR]"):
            if len(obj.ioscfg) > 0:
                for i1 in obj.ioscfg:
                    i2 = re.search(r":.*", i1)
                    i = i2.group()
                    generalVar.sn_text.append(ip + i)
            else:
                generalVar.failed_sn.append(ip)
        tn.close()
    except IOError:
        print('Also telnet unsucessfully:   ' + ip+'\n')
        generalVar.failed_sn.append(ip)
    except Exception:
        print('try another telnet')
        sn_telnet2(username, password, ip, commands)
    except:
        print('t2 '+ip+'\n')
        generalVar.failed_sn.append(ip)

def sn_telnet2(username, password, ip, commands):
    try:
        tn = telnetlib.Telnet(ip)
        print('Telenet sucessfully:   ' + ip)
        tn.read_until(b"username: ")
        tn.write(username.encode('ascii') + b'\n')
        tn.read_until(b"password: ")
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
        print(output)
        cfg = output.splitlines()
        parse = CiscoConfParse(cfg)
        for obj in parse.find_objects(
                    r"[sS][yY][sS][tT][eE][mM]\s*[Ss][eE][rR][iI][aA][lL]\s*[Nn][uU][mM][bB][eE][rR]"):
            if len(obj.ioscfg) > 0:
                for i1 in obj.ioscfg:
                    i2 = re.search(r":.*", i1)
                    i = i2.group()
                    generalVar.sn_text.append(ip + i)
            else:
                generalVar.failed_sn.append(ip)
        tn.close()
    except IOError:
        print('Also telnet unsucessfully:   ' + ip+'\n')
        generalVar.failed_sn.append(ip)
    except Exception:
        print('t1 '+ip+'\n')
        generalVar.failed_sn.append(ip)
    except:
        print('t2 '+ip+'\n')
        generalVar.failed_sn.append(ip)