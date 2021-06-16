import threading
import time
import sys
import os
import json

# 父级绝对路径 G:\Code\python\shell\monitor
work_dir = os.path.dirname(os.path.abspath(__file__))
# 把当前路径切换到文件所在的路径
os.chdir(work_dir)

root_dir = '../../../'

sys.path.append(root_dir)
from lib.helper import Helper
from lib.sina import Sina
from lib.workwx import WeChat


# 获取stock 列表
with open('../data/config/stock_config.json', 'r', encoding='utf-8') as f:
    stock_config = json.load(f)


# 钉钉机器人
def send_dingding_msg(content):
    # content: 发送内容
    # isAtAll: 是否要@某位用户
    json_data = {"msgtype": "text", "text": {"content": content}, "at": {"atMobiles": [], "isAtAll": False}}
    ding_url = 'https://oapi.dingtalk.com/robot/send?access_token=dfb241394310aeb3a94d32f1b359b7382429f4b435f9f0eb605979f50b21e857'
    # requests.post(url=ding_url, json=json_data)
    print('预警信息发送成功!')


# 企业微信
def send_workwx_msg(content):
    wx = WeChat()
    wx.send_markdown(content)


def cron_run():
    t = threading.Timer(0, event_func)
    t.setDaemon(True)
    t.start()


def event_func():
    print('running')


# 判断交易日
def to_break():
    ts = time.time()
    t = time.localtime(ts)
    tt = time.strftime("%H:%M:%S", t)
    dayofweek = t.tm_wday
    # 周六周日不交易
    if dayofweek > 4:
        return True
    # 处于交易时间段
    if "09:25:00" < tt < "15:00:00":
        return False

    return True


# 循环获取每个stock 数据
def loop_stock():
    cont_list = []
    sina = Sina()
    for row in stock_config['codes']:
        data = sina.get_stock_realtime(row['code'])
        print(data)
        exit()
        if row['rate'][0] < data['rate'] < row['rate'][1]:
            continue
        content = "预警：当前股票[{0}], 涨幅[{1}%], 请查收！【股票有风险，投资需谨慎】".format(data['name'], data['rate'])
        cont_list.append(content)
    return cont_list


def main():
    cont = loop_stock()
    print(cont)


if __name__ == '__main__':
    main()
