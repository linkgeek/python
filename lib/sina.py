import requests
from lib.helper import Helper
"""
新浪财经 
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
        # var hq_str_sz000725 = "京东方Ａ,7.330,7.260,7.320,7.480,7.220,7.320,7.330,839689831,6173688383.270,1
        # 768566, 7.320, 2015100, 7.310, 2700200, 7.300, 737100, 7.290, 1054400, 7.280, 370800, 7.330, 4124140, 7.340, 3558400, 7.350, 5271880, 7.360, 3972600, 7.370, 2021 - 04 - 30, 14: 48:36, 00
        # ";

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
        # 涨跌幅度
        rate = (now_price - prev_price) / prev_price * 100
        rate = Helper().float_format(rate)
        return {'code': code, 'name': name, 'open_price': open_price, 'prev_price': prev_price, 'max_price': max_price,
                'low_price': low_price, 'deal_num': deal_num, 'rate': rate}
