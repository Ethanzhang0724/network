# coding=utf-8
import socket
import generalVar
def scan_ports(target_host, port, queue):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.connect((target_host, port))
        print(port)
        generalVar.openports.append(port)
        sock.close()
    except (socket.timeout, ConnectionRefusedError):
        pass