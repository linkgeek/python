#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests
import json


class WeChat:
    def __init__(self):
        self.CORPID = 'ww1b0f2d1180d85f64'  # 企业ID，在管理后台获取
        self.CORPSECRET = 'BxQiJHBhuf4w9RMaqkU_vzxWaAmbmuntSy5oDtdBi1s'  # 自建应用的Secret，每个自建应用里都有单独的secret
        self.AGENTID = '1000023'  # 应用ID，在后台应用中获取
        self.TOUSER = "hezhan"  # 接收者用户名,多个用户用|分割

    # 获取新access_token
    def _get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,
                  'corpsecret': self.CORPSECRET,
                  }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    # 获取缓存access_token
    def get_access_token(self):
        try:
            with open('../data/workwx_access_token.conf', 'r') as f:
                t, access_token = f.read().split()
        except:
            with open('../data/workwx_access_token.conf', 'w') as f:
                access_token = self._get_access_token()
                cur_time = time.time()
                f.write('\t'.join([str(cur_time), access_token]))
                return access_token
        else:
            cur_time = time.time()
            if 0 < cur_time - float(t) < 7260:
                return access_token
            else:
                with open('../data/workwx_access_token.conf', 'w') as f:
                    access_token = self._get_access_token()
                    f.write('\t'.join([str(cur_time), access_token]))
                    return access_token

    # 发送信息
    def send_data(self, message):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        send_values = {
            "touser": self.TOUSER,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {
                "content": message
            },
            "safe": "0"
        }
        send_msges = (bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()  # 当返回的数据是json串的时候直接用.json即可将respone转换成字典
        return respone["errmsg"]


# if __name__ == '__main__':
#     wx = WeChat()
#     wx.send_data("这是程序发送的第1条消息！\n Python程序调用企业微信API,从自建应用“告警测试应用”发送给管理员的消息！")
#     wx.send_data("这是程序发送的第2条消息！")
