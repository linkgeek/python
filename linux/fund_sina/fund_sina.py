#!/usr/local/bin/python3
# 基金涨跌提醒 监控
import requests
from bs4 import BeautifulSoup
import re
import time
import json
import sys
import os

# 绝对路径
work_dir = os.path.dirname(os.path.abspath(__file__))
# 把当前路径切换到文件所在的路径
os.chdir(work_dir)

sys.path.append('../')
from api.workwx import WeChat

# 加载config
CONFIG = {}
# FUND_CONF = os.path.join(work_dir, 'fund_config.json')
with open('../data/fund_config.json', 'r', encoding='utf8') as f:
    CONFIG = json.load(f)


# 获取基金涨跌
def get_fund_rate(fund_code):
    """
    获取基金涨跌幅信息：信息来源（新浪财经 http://stocks.sina.cn/fund/）
    fund_code：为基金代码，若该基金不存在，返回 False，否则返回 涨跌幅比例
    """
    headers = {
        "Cookie": 'ustat=__14.28.56.65_1590560309_0.89300000; genTime=1590560309; SINAGLOBAL=4905578110989.475.1590560312465; Apache=3574138427052.4756.1595941642394; ULV=1595941642397:5:2:1:3574138427052.4756.1595941642394:1594733801049; sinaH5EtagStatus=y; vt=99; historyRecord={"href":"http://stocks.sina.cn/fund/","refer":""}',
        "Host": "stocks.sina.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
    }
    url = "http://stocks.sina.cn/fund/?code={}&vt=4#".format(fund_code)
    try:
        r = requests.get(url, headers)
        r.encoding = "UTF-8"
        soup = BeautifulSoup(r.text, "html.parser")
        result = soup.findAll(attrs={"class": "j_fund_valExt"})
        if len(result) == 1:
            pattern = "(?<=>)(.+)(?=<)"
            result = re.findall(pattern, str(result[0]))[0]
            return float(result.split("%")[0])
        else:
            return False
    except:
        return False


# 生成发送内容
def gen_cont():
    body_content = "<font color=\"comment\">Fund's latest warning {}</font>\n".format(
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    for obj in CONFIG['top']:
        code = obj['code']
        real_rate = get_fund_rate(code)
        if real_rate:
            rate = obj['rate']
            if rate[0] < real_rate and real_rate < rate[1]:
                continue

            # 根据基金代码获取基金信息
            headers = {
                "Cookie": "qgqp_b_id=f8b59df051caea02b176f6d76db75887; EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=null; EMFUND7=null; st_si=92310565820236; st_asi=delete; searchbar_code=160119; EMFUND0=null; EMFUND8=07-14%2021%3A54%3A31@%23%24%u5357%u65B9%u4E2D%u8BC1500ETF@%23%24510500; EMFUND9=07-25 23:07:36@#$%u5357%u65B9%u4E2D%u8BC1500ETF%u8054%u63A5A@%23%24160119; ASP.NET_SessionId=5ljqqn1s20zpfryhuw5fx4jw; st_pvi=06954122844047; st_sp=2020-05-20%2007%3A32%3A46; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=2; st_psi=20200725230736417-0-5210348614",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
            }
            url = "http://fund.eastmoney.com/js/fundcode_search.js"
            r = requests.get(url, headers)
            info = re.findall("(\[.*?\])", r.text[9:-2])
            fund_info = \
                list(filter(lambda x: x.replace("\"", "").replace("[", "").replace("]", "").split(",")[0] == code,
                            info))[0]
            ls = json.loads(fund_info)  # 将字符串转化为list格式
            if real_rate < rate[0]:
                temp = """CODE：{}，<font color=\"info\">↓</font>：<font color=\"info\">{}%</font>，POINT：{}%，ZH：{}\n""".format(
                    ls[0], real_rate, rate[0], ls[2])
            elif real_rate > rate[1]:
                temp = """CODE：{}，<font color=\"warning\">↑</font>：<font color=\"warning\">{}%</font>，POINT：<font color=\"warning\">{}%</font>，ZH：{}\n""".format(
                    ls[0], real_rate, rate[1], ls[2])
            else:
                temp = ''
        else:
            temp = """CODE：{}，<font color=\"comment\">failed to gain fund growth！！</font>\n""".format(code)

        if temp == '':
            temp = 'DATA IS EMPTY.'
        body_content += temp

    body_content += "\n[The stock market is risky, investment needs to be cautious]"
    return body_content


# 发送企业微信
def send_workwx_msg(content):
    wx = WeChat()
    wx.send_markdown(content)


def main():
    content = gen_cont()
    send_workwx_msg(content)


if __name__ == '__main__':
    main()
