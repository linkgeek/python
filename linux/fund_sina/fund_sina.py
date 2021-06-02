#!/usr/local/bin/python3
# 基金涨跌提醒 监控

import re
import time
import json
import sys
import os
import operator
import requests
from bs4 import BeautifulSoup

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


# 获取基金行情
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
        prev_growth = soup.findAll(attrs={"class": "stock_info_value"})
        if len(result) == 1:
            pattern = "(?<=>)(.+)(?=<)"
            result = re.findall(pattern, str(result[0]))[0]
            prev_growth = re.findall(pattern, str(prev_growth[0]))[0]
            return {'now': float(result.split("%")[0]), 'prev': float(prev_growth.split("%")[0])}
        else:
            return False
    except:
        return False


# load js
def download_js():
    filePath = '../data/fundcode_search.js'
    if os.path.isfile(filePath):
        return False

    headers = {
        "Cookie": "qgqp_b_id=f8b59df051caea02b176f6d76db75887; EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=null; EMFUND7=null; st_si=92310565820236; st_asi=delete; searchbar_code=160119; EMFUND0=null; EMFUND8=07-14%2021%3A54%3A31@%23%24%u5357%u65B9%u4E2D%u8BC1500ETF@%23%24510500; EMFUND9=07-25 23:07:36@#$%u5357%u65B9%u4E2D%u8BC1500ETF%u8054%u63A5A@%23%24160119; ASP.NET_SessionId=5ljqqn1s20zpfryhuw5fx4jw; st_pvi=06954122844047; st_sp=2020-05-20%2007%3A32%3A46; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=2; st_psi=20200725230736417-0-5210348614",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
    }
    url = "http://fund.eastmoney.com/js/fundcode_search.js"
    # r = requests.get(url, headers)
    # cont = re.findall('var r = (.*])', r.text)[0]  # 提取list
    # ls = json.loads(cont)  # 将字符串个事的list转化为list格式
    # all_fundCode = pd.DataFrame(ls, columns=['基金代码', '基金名称缩写', '基金名称', '基金类型', '基金名称拼音'])  # list转为DataFrame
    # print(all_fundCode)
    # exit()
    # info = re.findall("(\[.*?\])", r.text[9:-2])

    requests_info = requests.get(url, headers=headers)
    if requests_info.status_code == 200:
        html_bytes = requests_info.content
        html_str = html_bytes.decode()
        with open(filePath, 'w', encoding='utf8') as f:
            f.write(html_str)
    else:
        print(f'loadJs-error-{requests_info.status_code}')
    return True


# 修改json文件
def update_json():
    file_path = "../data/test_config.json"
    with open(file_path, "r", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)

    data["useCache"] = False
    data["top"][0]['remark'] = 'remark'
    data["location"] = "NewPath"

    with open(file_path, "w", encoding='utf-8') as jsonFile:
        json.dump(data, jsonFile, ensure_ascii=False)


# 生成发送内容
def gen_cont():
    rate_list = []
    for obj in CONFIG['top']:
        info = get_fund_rate(obj['code'])
        curr_rate = info['now']
        if curr_rate is not False:
            point_rate = obj['rate']
            if point_rate[0] < curr_rate < point_rate[1]:
                continue
        else:
            curr_rate = 0
        code_dict = {
            'code': obj['code'],
            'up': curr_rate,
            'rate': obj['rate'],
            'name': obj['name'],
            'prev': info['prev']
        }
        rate_list.append(code_dict)

    # 排序
    sort_list = sorted(rate_list, key=operator.itemgetter('up'), reverse=True)
    warn_text = ''
    for item in sort_list:
        temp = "Co：{}，".format(item['code'])
        if item['up'] > 0:  # 涨
            if item['prev'] >= 0:
                temp += "Pv：<font color=\"warning\">{}%</font>，".format(item['prev'])
            else:
                temp += "Pv：<font color=\"info\">{}%</font>，".format(item['prev'])
            temp += "<font color=\"warning\">↑</font>：<font color=\"warning\">{}%</font>，Po：{}%，Zh：{}\n""".format(
                format(item['up'], '.2f'), format(item['rate'][1], '.1f'), item['name'])
        elif item['up'] < 0:  # 跌
            if item['prev'] >= 0:
                temp += "Pv：<font color=\"warning\">{}%</font>，".format(item['prev'])
            else:
                temp += "Pv：<font color=\"info\">{}%</font>，".format(item['prev'])
            temp += "<font color=\"info\">↑</font>：<font color=\"info\">{}%</font>，Po：{}%，Zh：{}\n""".format(
                format(item['up'], '.2f'), format(item['rate'][0], '.1f'), item['name'])
        else:
            temp = """<font color=\"comment\">failed to gain fund growth！！</font>\n""".format(item['code'])
        warn_text += temp

    if len(warn_text) == 0:
        warn_text = "\nMessage is empty!\n"

    body_content = "<font color=\"comment\">Fund's latest warning {}</font>\n".format(
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    body_content += warn_text
    body_content += "\n<font color=\"comment\">[The stock market is risky, investment needs to be cautious]</font>"
    return body_content


# 发送企业微信
def send_work_wx(content):
    wx = WeChat()
    wx.send_markdown(content)


def main():
    # download_js()
    update_json()
    exit()
    content = gen_cont()
    send_work_wx(content)


if __name__ == '__main__':
    main()
