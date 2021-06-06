import socket

# 创建实例
sk = socket.socket()
# 定义绑定ip&port
ip_port = ('127.0.0.1', 8888)
# 绑定监听
sk.bind(ip_port)
# 最大连接数
sk.listen(5)
# 提示信息
print('正在进行等待接收数据....')
# 接收数据
conn, address = sk.accept()
# 定义信息
msg = "Hello World"
# 返回信息
conn.send(msg.encode())
# 主动关闭连接
conn.close()
