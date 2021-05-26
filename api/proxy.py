# --coding:utf-8--

import random
from urllib import request

# 代理ip
proxies = [
    '139.155.80.151:8000',
    '61.155.4.135:3128',
]


def proxy(url, headers):
    # 随机从IP列表中选择一个IP
    ip = random.choice(proxies)
    # 基于选择的IP构建连接
    handler = request.ProxyHandler({'http': ip})  # https://seofangfa.com/proxy/  （代理IP获取网址）
    opener = request.build_opener(handler)
    rq = request.Request(url, headers=headers)
    resp = opener.open(rq)
    return {'ip': ip, 'resp': resp.read()}


def main():
    url = 'http://httpbin.org/ip'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.51'
    }
    resp = proxy(url, headers)
    print(resp)


if __name__ == '__main__':
    main()
