import socket

client = socket.socket()

ip_port = ("127.0.0.1", 8888)

client.connect(ip_port)

data = client.recv(1024)

print(data.decode())
