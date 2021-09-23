#!/usr/bin/env python
import threading
import socket
 
def get_ip_status(ip, port, open_iplist):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.settimeout(0.5)
    try:
        server.connect((ip,port))
        print('{0} port {1} is open'.format(ip, port))
        open_iplist.append(ip)
    except Exception as err:
        print('{0} port {1} is not open'.format(ip,port))
    finally:
        server.close()
        
def get_host_ip(): 
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip
 
if __name__ == '__main__':
    host = get_host_ip()
    threads = []
    open_iplist = []
    for i in range(1,255):
        ip= ".".join(host.split(".")[0:3])+"."+str(i)
        t = threading.Thread(target=get_ip_status, args=(ip, 18622, open_iplist))
        threads.append(t)

    for t in threads:
        t.start()
        
    for t in threads:
        t.join()
        
    print(open_iplist)