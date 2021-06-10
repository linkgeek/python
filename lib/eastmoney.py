"""
天天基金网
"""

import re
import json
import time
import requests
import numpy as np
from bs4 import BeautifulSoup


class EastMoney:

    # 抓取网页
    @staticmethod
    def get_common_url(url, params=None, proxies=None):
        rsp = requests.get(url, params=params, proxies=proxies)
        rsp.raise_for_status()
        return rsp.text

    # 获取实时涨幅估值
    @staticmethod
    def get_realtime_rise_js(fund_code):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'
            }
            stamp = int(round(time.time() * 1000))
            url = f'http://fundgz.1234567.com.cn/js/{fund_code}.js?rt={stamp}'
            resp = requests.get(url, headers=headers)
            if resp.status_code == 200:
                data = json.loads(re.match(".*?({.*}).*", resp.text, re.S).group(1))
                # print('基金编码：%s' % data['fundcode'])
                # print('基金名称：%s' % data['name'])
                # print('单位净值：%s' % data['dwjz'])
                # print('净值日期：%s' % data['jzrq'])
                # print('估算值：%s' % data['gsz'])
                # print('估算增量：%s%%' % data['gszzl'])
                # print('估值时间：%s' % data['gztime'])
                # exit()
                return data
            else:
                print(f'loadJs-error-{resp.status_code}')
                return False
        except Exception as e:
            print('错误信息%s' % e)
            return False

    # 获取实时涨幅估值2[TODO]
    @staticmethod
    def get_realtime_rise_page(fund_code):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'
            }
            url = 'http://fund.eastmoney.com/%s.html' % fund_code
            resp = requests.get(url, headers=headers)
            print(time.time(), int(round(time.time() * 1000)))
            exit()
            # http://fundgz.1234567.com.cn/js/000001.js?rt=1623073418655  1623078163.8277621
            if resp.status_code == 200:
                resp.encoding = "UTF-8"
                soup = BeautifulSoup(resp.text, "html.parser")
                result = soup.findAll(attrs={"id": "gz_gszzl"})
                prev_growth = soup.findAll(attrs={"class": "ui-font-middle ui-color-red ui-num"})
                print(result)
                exit()
                return []
            return False
        except Exception as e:
            print('错误信息%s' % e)
            return False

    # 分页获取天天基金历史日增长率
    def get_rise_record(self, code, sdate, edate, per=10):
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
            page = page + 1
        return records
