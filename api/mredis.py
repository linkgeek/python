#!/usr/bin/python
# -*- coding: UTF-8 -*-
# https://mp.weixin.qq.com/s?__biz=MzU5NjM4MDY1Mw==&mid=2247490197&idx=1&sn=20a3e15ea4baea723705f713aabe0a9f&chksm=fe62c417c9154d015cf576fb730d020ceb296959ac3e8c4d2ff5aac9e85709054ebf5fd55559&cur_album_id=1575641054601674754&scene=189#rd

import redis


# redis类封装
class MyRedis:
    rd = None

    def __init__(self, host, port=6379):
        try:
            self.rd = redis.Redis(host=host, port=port, decode_responses=True, charset='UTF-8')
        except Exception as e:
            print('redis连接失败，错误信息%s' % e)
            return

    # str-set
    def str_set(self, key, value, time=None):
        self.rd.set(key, value, time)

    # str-get
    def str_get(self, key):
        return self.rd.get(key)

    def delete(self, key):
        flag = self.rd.exists(key)
        if flag:
            self.rd.delete(key)
