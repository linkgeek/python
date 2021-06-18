import requests
from lib.helper import Helper

"""
新浪财经 股票实时数据
"""


class Sina:
    # 获取stock 实时数据
    @staticmethod
    def get_stock_realtime(code):
        # https://hq.sinajs.cn/list=sz000725
        url = 'http://hq.sinajs.cn/list=' + code
        r = requests.get(url)
        res = r.text
        # print(res)
        # var hq_str_sh600905="三峡能源, 5.900, 5.450, 6.000, 6.000, 5.780, 6.000, 0.000, 582348566, ... ";

        result = res.split('=')[1]
        # 股票名称
        name = result.split(',')[0].replace('"', '')
        # 今日开盘价
        open_price = float(result.split(',')[1])
        # 昨日收盘价
        prev_price = float(result.split(',')[2])
        # 当前价格
        now_price = float(result.split(',')[3])
        # 今日最高价
        max_price = float(result.split(',')[4])
        # 今日最低价
        low_price = float(result.split(',')[5])
        # 成交的股票数
        deal_num = float(result.split(',')[8])
        hp = Helper()
        deal_num = hp.float_format(deal_num / 1000000)

        # 涨跌幅度
        rate = (now_price - prev_price) / prev_price * 100
        rate = hp.float_format(rate)
        return {'code': code, 'name': name, 'open_price': open_price, 'prev_price': prev_price, 'max_price': max_price,
                'low_price': low_price, 'now_price': now_price, 'deal_num': deal_num, 'rate': rate}
