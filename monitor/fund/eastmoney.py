#!/usr/local/bin/python3
"""
天天基金 涨跌估值 提醒监控
"""

import time
import json
import sys
import os
import operator

work_dir = os.path.dirname(os.path.abspath(__file__))
# 把当前路径切换到文件所在的路径
os.chdir(work_dir)

sys.path.append('../../')
from lib.eastmoney import EastMoney
from lib.helper import Helper
from lib.workwx import WeChat

# 加载config
CONFIG = {}
# FUND_CONF = os.path.join(work_dir, 'fund_config.json')
with open('../data/config/fund_config.json', 'r', encoding='utf8') as f:
    CONFIG = json.load(f)


# 获取基金涨幅
def get_fund_rise(fund_code):
    em = EastMoney()
    # 实时估值
    gz = em.get_realtime_rise_js(fund_code)
    # print(gz)
    # 历史交易日涨幅
    record = em.get_rise_record(fund_code, gz['jzrq'], gz['jzrq'])
    prev_rise = record[0][3]
    return float(gz['gszzl']), float(prev_rise.split("%")[0])


# 生成发送内容
def gen_cont(key='hold', show_all=False):
    rate_list = []
    hp = Helper()
    for obj in CONFIG[key]:
        print(f'loading......{obj["code"]}')
        curr_rise, prev_rise = get_fund_rise(obj['code'])
        if curr_rise is not False:
            point_rate = obj['rate']
            if point_rate[0] < curr_rise < point_rate[1] and show_all is False:
                continue
        else:
            curr_rise = 0

        code_dict = {
            'code': obj['code'],
            'up': curr_rise,
            'rate': obj['rate'],
            'name': obj['name'],
            'prev': prev_rise
        }
        rate_list.append(code_dict)

    # 排序
    sort_list = sorted(rate_list, key=operator.itemgetter('up'), reverse=True)
    warn_text = ''
    for item in sort_list:
        temp = "Co：{}，".format(item['code'])
        # 昨天
        if item['prev'] >= 0:
            temp += "Pv：<font color=\"warning\">{}%</font>，".format(item['prev'])
        else:
            temp += "Pv：<font color=\"info\">{}%</font>，".format(item['prev'])
        # 涨跌
        if item['up'] > 0:  # 涨
            temp += "<font color=\"warning\">↑：{}%</font>，Zh：{}\n""".format(hp.float_format(item['up']), item['name'])
        elif item['up'] < 0:  # 跌
            temp += "<font color=\"info\">↓：{}%</font>，Zh：{}\n""".format(hp.float_format(item['up']), item['name'])
        else:
            temp = """<font color=\"comment\">failed！！</font>\n""".format(item['code'])
        warn_text += temp

    if len(warn_text) == 0:
        warn_text = "\nMessage is empty!\n"

    body_content = "<font color=\"comment\">EM Fund's Report{}</font>\n".format(
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    body_content += warn_text
    body_content += "\n<font color=\"comment\">[The stock market is risky, investment needs to be cautious]</font>"
    return body_content


# 发送企业微信
def send_work_wx(content):
    wx = WeChat()
    wx.send_markdown(content)


def main():
    content = gen_cont('hold', True)
    # print(content)
    # exit()

    send_work_wx(content)


if __name__ == '__main__':
    main()
