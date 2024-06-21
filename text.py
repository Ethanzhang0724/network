'''import sqlite3

db=sqlite3.connect("cisco.db")
cs=db.cursor()
#cs.execute('insert into tb_user (username, userpwd) values ("zhang","Pirelli001")')
cs.execute('select * from tb_user')
print(cs.fetchall()) '''


from netaddr import *
import re
mac1="90-78-41-DE-17-23"
macs=[]

mac=EUI(mac1)
mac.dialect=mac_cisco
macs.append(mac)
for i in macs:
    print(i)

mac='1.1.1'

'''commands=['end'," show mac address-table | include "+mac]
print(commands)'''

#pattern = r"(Te|Gi|Fa|Po)\S*\d"
'''pattern=r"IP address:\s*(\S*)"

output="CN-PIR-SHANGHAI-BB148.2#sh cdp neighbors T1/1/4 detail Device ID: CN-PIR-SHANGHAI-BB148.3.pirelli.com  Entry address(es):" \
       "IP address: 10.130.148.3  "  \
"Platform: cisco C9300-48P,  Capabilities: Router Switch IGMP " \

"Interface: TenGigabitEthernet1/1/4,  Port ID (outgoing port): TenGigabitEthernet1/1/4" \
"Holdtime : 148 sec"  \
  "IP address: 10.130.148.3 " \''''
'''output="CN-PIR-SHANGHAI-BB148.2#sh etherchannel summary | include  " \
       "10     P10(SU)        LACP      "
#i = re.findall(patten, output,)


i=re.search(pattern,output)

if i==None:
       print('suck')
print(i.group())

if 'Po' in i.group():
       print('Po')'''

#output="Platform: cisco WS-C2960X-12S"


'''pattern=r"(Catalyst|2960|3750)"
result=re.search(pattern,output,re.I)
print(result)
print(result.group())'''

#pattern=r"system\s*serial\s*number\s*:\s*(\S*)|board\s*ID\s*(\S*)"
'''output="cisco ISR4331/K9 (1RU) processor with 1793357K/6147K bytes of memory. " \
       "   Processor board ID FDO2129A0E1 "
pattern = r"IP.*?address:\s*(\S*)"
output2="IP address: 10.130.203.7  dd address 1010.1.1.1"
output1="Model Number                       : C9300-48P" \
        "  System Serial Number               : FOC2311U0L4"
result=re.search(pattern,output2,re.I)

print(result.group(1))'''
'''pa=r"\S{4}\.\S{4}\.\S{4}"
p2=r"[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}"
ou1="   000c.295e.94aa  ARPA  "
ou="Internet CN-PIR-SHANGHA  10.130.148.79   2  000c.295e.94aa  ARPA   Vlan2"
i=re.search(pa,ou)
print(i.group())'''