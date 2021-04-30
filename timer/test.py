from threading import Timer
import time

def hello():
    print("hello, world")


def run_one():
    # 指定2秒后执行hello函数
    t = Timer(2.0, hello)
    t.start()


def main():
    run_one()


if __name__ == '__main__':
    main()