#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
企业微信接口
"""
import os
import time
import requests
import json

work_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(work_dir)


class WeChat:
    def __init__(self):
        self.URI = 'https://qyapi.weixin.qq.com/cgi-bin/'
        self.CORPID = 'ww1b0f2d1180d85f64'  # 企业ID，在管理后台获取
        self.CORPSECRET = 'tg6OPTwzBS0j5k6477qi5ri-UFhnEO00EcqKuWuM5TY'  # 自建应用的Secret，每个自建应用里都有单独的secret
        self.AGENTID = '1000024'  # 应用ID，在后台应用中获取  平台系统通知：1000023 BxQiJHBhuf4w9RMaqkU_vzxWaAmbmuntSy5oDtdBi1s
        self.TOUSER = "hezhan"  # 接收者用户名,多个用户用|分割

    # 获取新access_token
    def _get_access_token(self):
        url = self.URI + 'gettoken'
        values = {'corpid': self.CORPID, 'corpsecret': self.CORPSECRET}
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    # 获取缓存access_token
    def get_access_token(self):
        try:
            with open('../data/config/workwx_access_token.conf', 'r') as f:
                t, access_token = f.read().split()
        except:
            with open('../data/config/workwx_access_token.conf', 'w') as f:
                access_token = self._get_access_token()
                cur_time = time.time()
                f.write('\t'.join([str(cur_time), access_token]))
                return access_token
        else:
            cur_time = time.time()
            if 0 < cur_time - float(t) < 7260:
                return access_token
            else:
                with open('../data/config/workwx_access_token.conf', 'w') as f:
                    access_token = self._get_access_token()
                    f.write('\t'.join([str(cur_time), access_token]))
                    return access_token

    # 发送纯文本信息
    def send_text(self, message):
        send_url = self.URI + 'message/send?access_token=' + self.get_access_token()
        send_values = {
            "touser": self.TOUSER,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {
                "content": message
            },
            "safe": "0"
        }
        send_msg = (bytes(json.dumps(send_values), 'utf-8'))
        resp = requests.post(send_url, send_msg)
        resp = resp.json()  # 当返回的数据是json串的时候直接用.json即可将response转换成字典
        return resp["errmsg"]

    # 发送markdown消息
    def send_markdown(self, message):
        send_url = self.URI + 'message/send?access_token=' + self.get_access_token()
        send_values = {
            "touser": self.TOUSER,
            "msgtype": "markdown",
            "agentid": self.AGENTID,
            "markdown": {
                "content": message
            },
            "safe": "0"
        }
        send_msg = (bytes(json.dumps(send_values), 'utf-8'))
        resp = requests.post(send_url, send_msg)
        resp = resp.json()
        return resp["errmsg"]
