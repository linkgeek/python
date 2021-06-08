import random
import socketserver


# 定义一个类
class MyServer(socketserver.BaseRequestHandler):
    # 如果handle方法出现报错，则会进行跳过
    # setup方法和finish方法无论如何都会进行执行的
    # 首先执行setup
    def setup(self):
        pass

    # 然后执行handle
    def handle(self):
        # 定义连接变量
        conn = self.request
        msg = "Hello World!"
        conn.send(msg.encode())
        while True:
            data = conn.recv(1024)
            print(data.decode())
            if data == b'exit':
                break
            conn.send(data)
            conn.send(str(random.randint(1, 1000)).encode())
        conn.close()

    def finish(self):
        pass


if __name__ == "__main__":
    # 创建多线程实例
    server = socketserver.ThreadingTCPServer(("127.0.0.1", 8888), MyServer)
    # 开启异步多线程，等待连接
    print('开启异步多线程，等待连接.....')
    server.serve_forever()
