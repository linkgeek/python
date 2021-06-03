#!/usr/bin/python
# -*- coding: UTF-8 -*-
# https://mp.weixin.qq.com/s?__biz=MzU5NjM4MDY1Mw==&mid=2247490197&idx=1&sn=20a3e15ea4baea723705f713aabe0a9f&chksm=fe62c417c9154d015cf576fb730d020ceb296959ac3e8c4d2ff5aac9e85709054ebf5fd55559&cur_album_id=1575641054601674754&scene=189#rd

import redis
import sys
import os

# 绝对路径
work_dir = os.path.dirname(os.path.abspath(__file__))
# 把当前路径切换到文件所在的路径
os.chdir(work_dir)

sys.path.append('../')
from api.mredis import MyRedis

# 接口
mr = MyRedis('192.168.7.26')
mr.str_set('hhhhh', '666888')
print(mr.str_get('hhhhh'))
mr.delete('hhhhh')
print(mr.str_get('hhhhh'))
print('--------------------------华丽的分割线----------------------------')

# 普通连接
r = redis.Redis(host="192.168.7.26", port=6379, decode_responses=True, charset='UTF-8')

# 连接池: 避免每次建立、释放连接带来的开销
# pool = db.ConnectionPool(host='192.168.7.26', port=6379)
# r = db.Redis(connection_pool=pool)

# [set]
r.set('name1', 'chenge')  # 添加
r.set('name2', '辰哥')  # 添加

# 设置过期时间（秒），5秒过期
r.setex('key1', 5, 'value1')

# 设置过期时间（毫秒），1000毫秒过期
r.psetex("key2", 1000, "value2")

print(r.get('name1'))  # 获取
print(r.get('name2'))  # 获取

print('--------------------------华丽的分割线----------------------------')

# [mset]
r.mset({'key3': 'value3', 'key4': 'value4'})
print(r.get('key3'))
print(r.get('key4'))

# [mget]
print(r.mget("key3", "key4"))

print('--------------------------华丽的分割线----------------------------')
