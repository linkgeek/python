#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests, json


def requestWeb(url, server, cmd, data):
    s = json.dumps({
        "server": server,
        "cmd": cmd,
        "data": data,
    })

    return json.loads(requests.post(url, s).text)

# if __name__ == "__main__":
#     # test 
#     print(requestWeb("http://192.168.6.88:9600", "hall", "detachWechat", {
#         "guid": 9000000001,
#     }))
