import socket

sk = socket.socket()
ip_port = ("127.0.0.1", 8111)
sk.connect(ip_port)

with open('serv.py', 'rb') as f:
    for i in f:
        sk.send(i)
        data = sk.recv(1024)
        if data != b'success':
            break
sk.send('quit'.encode())
