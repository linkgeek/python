import os
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import json


class Fund:
    def __init__(self):
        pass

    # 抓取网页
    def get_common_url(self, url, params=None, proxies=None):
        rsp = requests.get(url, params=params, proxies=proxies)
        rsp.raise_for_status()
        return rsp.text

    # 分页获取天天基金历史日增长率
    def get_east_rise_record(self, code, sdate, edate, per=10):
        url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx'
        params = {'type': 'lsjz', 'code': code, 'page': 1, 'per': per, 'sdate': sdate, 'edate': edate}
        html = self.get_common_url(url, params)
        soup = BeautifulSoup(html, 'html.parser')

        # 获取总页数
        pattern = re.compile(r'pages:(.*),')
        result = re.search(pattern, html).group(1)
        pages = int(result)

        # 获取表头
        heads = []
        for head in soup.findAll("th"):
            heads.append(head.contents[0])

        # 数据存取列表
        records = []

        # 从第1页开始抓取所有页面数据
        page = 1
        while page <= pages:
            params = {'type': 'lsjz', 'code': code, 'page': page, 'per': per, 'sdate': sdate, 'edate': edate}
            html = self.get_common_url(url, params)
            soup = BeautifulSoup(html, 'html.parser')

            # 获取数据
            for row in soup.findAll("tbody")[0].findAll("tr"):
                row_records = []
                for record in row.findAll('td'):
                    val = record.contents
                    # 处理空值
                    if not val:
                        row_records.append(np.nan)
                    else:
                        row_records.append(val[0])

                # 记录数据
                records.append(row_records)
            # 下一页
            page = page + 1

        # 数据整理到dataFrame
        np_records = np.array(records)
        data = pd.DataFrame()
        for col, col_name in enumerate(heads):
            data[col_name] = np_records[:, col]
        return data

    # 获取基金1周-5年涨幅[蛋卷]
    def get_danjuan_history_rise(self, code):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
        }
        fu_url = "https://danjuanapp.com/djapi/fund/derived/" + str(code)
        res = requests.get(fu_url, headers=headers)
        res.encoding = 'utf-8'
        s = json.loads(res.text)
        data = s['data']

        values = []

        # 防止基金最长时间不够1年、2年、5年的情况报错，用0填充
        # 近1周
        try:
            values.append(data['nav_grl1w'])
        except:
            values.append(0)
        # 近1月
        try:
            values.append(data['nav_grl1m'])
        except:
            values.append(0)
        # 近3月
        try:
            values.append(data['nav_grl3m'])
        except:
            values.append(0)
        # 近6月
        try:
            values.append(data['nav_grl6m'])
        except:
            values.append(0)
        # 近1年
        try:
            values.append(data['nav_grl1y'])
        except:
            values.append(0)
        # 近3年
        try:
            values.append(data['nav_grl3y'])
        except:
            values.append(0)
        # 近5年
        try:
            values.append(data['nav_grl5y'])
        except:
            values.append(0)

        return values
