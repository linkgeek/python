import socket

# 实例初始化
client = socket.socket()
ip_port = ("127.0.0.1", 8888)
client.connect(ip_port)

while True:
    data = client.recv(1024)
    print(data.decode())
    msg_input = input("请输入发送的信息：")
    client.send(msg_input.encode())
    if msg_input == "quit":
        break
    data = client.recv(1024)
    print(data.decode())
