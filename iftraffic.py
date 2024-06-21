# coding=utf-8
import re
import pandas as pd
import netmiko
import paramiko
import generalVar
import socket

def if_ssh(username, password, ip, commands, secret,date, dic, f1 ,queue2, ios='cisco_ios'):
    try:
        sw = {'device_type': ios, 'ip': ip, 'username': username, 'password': password, 'secret': secret}
        connect = netmiko.ConnectHandler(**sw)  ## 字典赋值用** , 列表用*
        connect.enable()
        output = connect.send_config_set(commands)
        cfg = output.splitlines()
        for i, n in enumerate(cfg):
            if "RXPS" in n and "TXPS" in n:
                break
        coloumns = re.split(r'\s+', cfg[i])
        data = []
        for dd in cfg[i+2:-1]:
            data1 = re.split(r'\s+', dd)
            data.append(data1)

        pd.set_option('display.max_columns', 500)
        pd.set_option('display.max_rows', 1000)
        pd.set_option('display.width', 1000)
        pd.set_option('display.unicode.ambiguous_as_wide', True)
        pd.set_option('display.unicode.east_asian_width', True)
        df = pd.DataFrame(data=data,columns=coloumns)
        #df.columns = coloumns
        df['RXPS']=df['RXPS'].astype('int')
        df=df.sort_values(by=['RXPS'],axis=0, ascending=False)
        #df.to_excel(f,sheet_name='interface')

        with open(dic+"\\"+date+"_"+ip+'_interfaces.txt','a+') as f:
            f.write('\n' + str(df))

        generalVar.interface_text=df[['Interface','RXPS']]

    except netmiko.ssh_exception.NetmikoAuthenticationException:
        print('未知异常 ' + ip + '\n')
        f1.write(ip + '\n')
    except netmiko.ssh_exception.NetmikoTimeoutException:
        print('unreachable ip,will try telnet:   ' + ip + '\n')

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


def if_ssh1(username, password, ip, commands, secret , queue2, ios='cisco_ios'):
    try:
        sw = {'device_type': ios, 'ip': ip, 'username': username, 'password': password, 'secret': secret}
        connect = netmiko.ConnectHandler(**sw)  ## 字典赋值用** , 列表用*
        connect.enable()
        output = connect.send_config_set(commands)
        cfg = output.splitlines()
        for i, n in enumerate(cfg):
            if "RXPS" in n and "TXPS" in n:
                break
        coloumns = re.split(r'\s+', cfg[i])
        data = []
        for dd in cfg[i+2:-1]:
            data1 = re.split(r'\s+', dd)
            data.append(data1)

        pd.set_option('display.max_columns', 500)
        pd.set_option('display.max_rows', 1000)
        pd.set_option('display.width', 1000)
        pd.set_option('display.unicode.ambiguous_as_wide', True)
        pd.set_option('display.unicode.east_asian_width', True)
        df = pd.DataFrame(data=data, columns=coloumns)
        # df.columns = coloumns
        print(df['RXPS'])
        df['RXPS'] = df['RXPS'].astype('int')
        df = df.sort_values(by=['RXPS'], axis=0, ascending=False,ignore_index=False)
        generalVar.interface_text = df[['Interface', 'RXPS']]

    except netmiko.ssh_exception.NetmikoAuthenticationException:
        print('未知异常 ' + ip + '\n')
        generalVar.failed_interface.append(ip)
    except netmiko.ssh_exception.NetmikoTimeoutException:
        print('unreachable ip,will try telnet:   ' + ip + '\n')
        # f1.write(ip + '\n')
        generalVar.failed_interface.append(ip)
    except socket.error:
        print('file Path not found: ' + ip + '\n')
        generalVar.failed_interface.append(ip)
    except netmiko.NetMikoAuthenticationException:
        print("1:    " + ip + '\n')
        generalVar.failed_interface.append(ip)
    except netmiko.ssh_exception.AuthenticationException:
        print('密码错误或者未启用tacas导致登录失败:     ' + ip + '\n')
        generalVar.failed_interface.append(ip)
    except paramiko.ssh_exception.SSHException:
        print('SSH Unenabled,try to login with Telnet:  ' + ip + '\n')
        # self.f1.write(self.ip + '\n')
        generalVar.failed_interface.append(ip)
    except netmiko.ssh_exception.SSHException:
        print('4:   ' + ip + '\n')
        generalVar.failed_interface.append(ip)
    except netmiko.ssh_autodetect:
        print('5:   ' + ip + '\n')
        generalVar.failed_interface.append(ip)
    except Exception:
        print('6:   ' + ip + '\n')
        generalVar.failed_interface.append(ip)
    except:
        print('7:    ' + ip + '\n')


