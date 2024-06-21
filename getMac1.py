# coding=utf-8
import netmiko
import paramiko
import re
from tkinter.messagebox import *
import generalVar
import socket


def run(username, password, ip, mac, secret, ios):
    try:
        global connect
        global commands

        sw = {'device_type': ios, 'ip': ip, 'username': username,
              'password': password, 'secret': secret}
        connect = netmiko.ConnectHandler(**sw)  ## 字典赋值用** , 列表用*
        connect.enable()
        commands=["do sh mac address-table | include "+mac,'end']
        output = connect.send_config_set(commands)
       #connect.disconnect()
        patten = r"(Te|Gi|Fa|Po|Eth|Fo)\S*\d"
        interface = re.search(patten, output)
        if interface is None:
            generalVar.mac_text = mac + ' NOT Found'
            print('dff')
            print(generalVar.mac_text)
        elif 'Po' in interface.group():
            print('suck')
            patten = r"\w+?(\d+)"
            inter = re.search(patten, interface.group(), re.I)
            print(inter.group(1))
            command = "show port-channel summary | include Po" + inter.group(1)
            output = connect.send_command(command)
            pattern = r"(Te|Gi|Fa|Eth|Fo)\S*\d"
            interface = re.search(pattern, output,re.I)
            cdp(username, password, ip,mac, secret, ios,interface.group())
        else:
            cdp(username, password, ip,mac, secret, ios,interface.group())
    except netmiko.ssh_exception.NetmikoAuthenticationException:
        generalVar.mac_text='未知异常 ' + ip + '\n'
    except netmiko.ssh_exception.NetmikoTimeoutException:
        generalVar.mac_text='unreachable ip,will try telnet:   ' + ip + '\n'
    except socket.error:
        generalVar.mac_text='file Path not found: ' + ip + '\n'
    except netmiko.NetMikoAuthenticationException:
        print("1:    " + ip + '\n')
    except netmiko.ssh_exception.AuthenticationException:
        generalVar.mac_text='密码错误或者未启用tacas导致登录失败:     ' + ip + '\n'
    except paramiko.ssh_exception.SSHException:
        generalVar.mac_text='SSH Unenabled,try to login with Telnet:  ' + ip + '\n'
    except netmiko.ssh_exception.SSHException:
        generalVar.mac_text='4:   ' + ip + '\n'
    except netmiko.ssh_autodetect:
        generalVar.mac_text='5:   ' + ip + '\n'
    except Exception:
        generalVar.mac_text='6:   ' + ip + '\n'
    except:
        print('7:    ' + ip + '\n')
        showwarning('警告', '运行错误')


def cdp(username, password,ipc, mac, secret, ios,interface):
    try:
        output = connect.send_command("show cdp neighbors interface " + interface + " detail")
        connect.disconnect()
        pattern = r"(Catalyst|2960|3750|3850|Nexus)"
        result = re.search(pattern, output, re.I)
        if result is not None:
            pattern = r"IP.*?address:\s*(\S*)"
            ip1 = re.search(pattern, output,re.I)
            ip = ip1.group(1)
            run(username, password, ip, mac, secret, ios)
        else:
            output1 = "Connected Switch：" + ipc + '\n' + 'Switch port：' + interface
            generalVar.mac_text = output1

    except:
        showerror("warning",'cdp发现错误')


