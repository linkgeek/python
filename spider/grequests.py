# coding:utf-8
import grequests
import time
import json
import requests

adata = json.dumps({"key": "value"})
header = {"Content-type": "appliaction/json", "Accept": "application/json"}


def use_grequests(num):
    task = []
    urls = ["http://hao.jobbole.com/python-docx/" for i in range(num)]
    while urls:
        url = urls.pop(0)
        rs = grequests.post(url, data=adata, headers=header)
        task.append(rs)
    resp = grequests.map(task, size=5)
    return resp


def use_requests(num):
    urls = ["http://hao.jobbole.com/python-docx/" for i in range(num)]
    index = 0
    while urls:
        url = urls.pop(0)
        resp = requests.post(url=url, headers=header, data=adata)
        index += 1
        if index % 10 == 0:
            print('目前是第{}个请求'.format(index))


def main(num):
    print('正在使用requests模块发起请求...')
    time1 = time.time()
    finall_res = use_requests(num)
    print(finall_res)
    time2 = time.time()
    T = time2 - time1
    print('use_requests发起{}个请求花费了{}秒'.format(num, T))

    print('正在使用grequests模块发起请求...')
    time3 = time.time()
    finall_res2 = use_grequests(num)
    print(finall_res2)
    time4 = time.time()
    T2 = time4 - time3
    print('use_grequests发起{}个请求花费了{}秒'.format(num, T2))


if __name__ == '__main__':
    main(100)
