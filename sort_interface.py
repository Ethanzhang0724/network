# coding=utf-8
import re
import pandas as pd
import time
from datetime import datetime
output = open("C:\\APP\\interface.txt",'r')
cfg = output.read().splitlines()
now=datetime.now()
date = '%s-%s-%s' % (now.year, now.month, now.day)
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

with open("C:\\APP\\"+date+"_"+'_interfaces.txt','w+') as f:
    f.write('\n' + str(df))

output.close()




