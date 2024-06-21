from pythonping import *
import generalVar
def getonline(ip1, queue1):
    result = ping(ip1, count=2, timeout=1)
    if 'Reply' in str(result):
        print('Online:  ' + ip1 + '\n')
        generalVar.online_text.append(ip1)
    else:
        print("offline:  " + ip1 + '\n')
