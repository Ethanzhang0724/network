import socket
import generalVar
def scanports(host, port, queue):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.connect((host, port))
        generalVar.openports.append(port)
        sock.close()
    except (socket.timeout, ConnectionRefusedError):
        pass
