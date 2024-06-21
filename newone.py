# coding=utf-8
import netmiko

sw2={"device_type":"cisco_ios","ip":"10.130.148.4", "username":"zhangyi006", "password":"Bayer2015"}
try:
    connect = netmiko.ConnectHandler(**sw2)
    #connect=netmiko.ConnLogOnly(**sw2)
    output = connect.send_command('do show version')
    print(output)
except:
    print('fialed')