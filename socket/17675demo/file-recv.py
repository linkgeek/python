import socket

sk = socket.socket()
ip_port = ("127.0.0.1", 8111)
sk.connect(ip_port)

sk.listen(5)

while True:
    conn, address = sk.accept()
    while True:
        with open('file', 'ab') as f:
            data = conn.recv(1024)
            if data == b'quit':
                break
            f.write(data)
        conn.send('success'.encode())
    print('文件接收完成')
sk.close()
