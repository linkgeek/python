import requests
import json


# 蛋卷基金爬虫
class DanJuan:
    def __init__(self):
        self.api = 'https://danjuanapp.com/djapi/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
        }

    def get_common_url(self, url):
        resp = requests.get(url, headers=self.headers)
        resp.encoding = 'utf-8'
        return json.loads(resp.text)

    # 获取1周-成立以来收益
    def get_history_yield(self, code):
        url = "https://danjuanapp.com/djapi/fund/derived/" + str(code)
        resp = requests.get(url, headers=self.headers)
        resp.encoding = 'utf-8'
        s = json.loads(resp.text)
        data = s['data']

        values = []
        time_map = {
            'nav_grl1w': '近1周',
            'nav_grl1m': '近1月',
            'nav_grl3m': '近3月',
            'nav_grl6m': '近6月',
            'nav_grl1y': '近1年',
            'nav_grl2y': '近2年',
            'nav_grl3y': '近3年',
            'nav_grl5y': '近5年',
            'nav_grbase': '成立以来',
            'end_date': '截止时间',
        }

        # 防止基金最长时间不够1年、2年、5年的情况报错，用0填充
        for key, val in time_map.items():
            try:
                values.append(data[key])
            except:
                values.append(0)

        return values

    # 获取基金历史交易日净值、涨幅情况
    def get_daily_record(self, code, size=30, get_all=True):
        url = self.api + "fund/nav/history/" + str(code) + "?size=" + str(size) + "&page=1"
        s = self.get_common_url(url)
        if s['result_code'] != 0:
            return False

        percentage = []
        date = []
        value = []

        # 从第1页开始抓取所有页面数据
        page = 1
        total_pages = s['data']['total_pages']
        while page <= total_pages:
            url = self.api + "fund/nav/history/" + str(code) + "?size=" + str(size) + "&page=" + str(page)
            s = self.get_common_url(url)
            items = s['data']['items']
            for k in range(0, len(items)):
                date.append(items[k]['date'])  # 日期
                value.append(items[k]['nav'])  # 净值
                percentage.append(items[k]['percentage'])  # 涨跌
            # 只获取一页
            if get_all is False:
                break

        return date, value, percentage

    # 获取某类基金某阶段涨跌幅top10
    def filter_yield_top10(self, f_type=3, order='1w'):
        url = self.api + "v3/filter/fund?type=" + str(f_type) + "&order_by=" + order + "&size=10&page=1"
        res = requests.get(url, headers=self.headers)
        res.encoding = 'utf-8'
        s = json.loads(res.text)
        s = s['data']['items']
        name = []
        value = []
        for i in range(0, len(s)):
            code = s[i]['fd_code']
            name.append(s[i]['fd_name'] + "\n" + code)
            value.append(s[i]['yield'])
        return value, name
