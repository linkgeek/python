import requests
import json


# 蛋卷基金爬虫
class DanJuan:
    def __init__(self):
        pass

    # 获取1周-5年历史涨幅
    @staticmethod
    def get_history_rise(code):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
        }
        fu_url = "https://danjuanapp.com/djapi/fund/derived/" + str(code)
        res = requests.get(fu_url, headers=headers)
        res.encoding = 'utf-8'
        s = json.loads(res.text)
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
