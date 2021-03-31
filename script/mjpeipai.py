#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests, json, web

# web 服地址
weburl = "http://39.108.81.164:9600"

# 同步通用产品配牌配置到红幺鸡配牌
if __name__ == "__main__":
    d = web.requestWeb(weburl, "configuration", "updateConfigV3", {
        "table": "t_room_config", 
        "opr": "getkey",
        "key": "majong.peipai",        
        "subkey": "",
        "product": 0,
        "channel": 0,
        "prov": 0,
        "city": 0,        
        "area": 0,
    })

    for v in d['data']:
        if v['productID'] != 0:
            continue

        cmd = web.requestWeb(weburl, "configuration", "updateConfigV3" , {
            "table": "t_room_config", 
            "opr": "add",
            "key": "majong.peipai",        
            "subkey": v['subkey'],
            "value": v['value'],
            "product": 9999,
            "channel": 0,
            "prov": 0,
            "city": 0,        
            "area": 0,
            "user": "system" 
        })
        print( u"%s 同步结果: %s。 配置值: %s" ) % (v['subkey'], json.dumps(cmd).encode('utf-8'), v['value'])

