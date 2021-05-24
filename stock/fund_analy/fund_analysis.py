# coding: utf-8
# 分析基金 基金对比 基金业绩
import random
import requests
import time
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import json
import re
import matplotlib.pyplot as plt
import os
import lxml.html

# 绝对路径
work_dir = os.path.dirname(os.path.abspath(__file__))
# 把当前路径切换到文件所在的路径
os.chdir(work_dir)

DATA_PATH = '../../data/'
PATH_CACHE = DATA_PATH + 'fund_cache'

# 显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决负号“-”显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

CONFIG = {}
with open(DATA_PATH + 'stock_fund/fund_config.json', 'r', encoding='utf8') as f:
    CONFIG = json.load(f)


# print(CONFIG)
# exit()


def downloadJson(fundCode):
    # filePath = f'./cache/{fundCode}.json'
    filePath = f'{PATH_CACHE}/{fundCode}.json'
    if (CONFIG['useCache'] and os.path.isfile(filePath)):
        return False

    requests_url = 'http://api.fund.eastmoney.com/pinzhong/LJSYLZS'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        'Accept': 'application/json',
        'Referer': f'http://fund.eastmoney.com/{fundCode}.html',
    }
    params = {
        'fundCode': f'{fundCode}',
        'indexcode': '000300',
        'type': 'try',
    }
    requests_page = requests.get(requests_url, headers=headers, params=params)
    if requests_page.status_code == 200:
        with open(filePath, 'w', encoding='utf8') as f:
            json.dump(requests_page.json(), f)
    else:
        print(f'{requests_url}-{requests_page.status_code}')
    return True


# /*基金或股票信息*/
# var fS_name = "国联安精选混合"
# var fS_code = "257020"
# /*原费率*/
# var fund_sourceRate = "1.50"
# /*近一年收益率*/
# var syl_1n = "23.5593"
# /*近6月收益率*/
# var syl_6y = "18.9233"
# /*近三月收益率*/
# var syl_3y = "-1.4865"
# /*近一月收益率*/
# var syl_1y = "-0.2736"
# /*现费率*/
# var fund_Rate = "0.15"
# /*规模变动 mom-较上期环比*/
# var Data_fluctuationScale
def downloadJs(fundCode):
    filePath = f'{PATH_CACHE}/{fundCode}.js'
    if (CONFIG['useCache'] and os.path.isfile(filePath)):
        return False
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
    }
    requests_info = requests.get(f'http://fund.eastmoney.com/pingzhongdata/{fundCode}.js', headers=headers)
    if requests_info.status_code == 200:
        html_bytes = requests_info.content
        html_str = html_bytes.decode()
        with open(filePath, 'w', encoding='utf8') as f:
            f.write(html_str)
    else:
        print(f'requests_info-{requests_info.status_code}')
    return True


def downloadHtml(fundCode):
    filePath = f'{PATH_CACHE}/jjfl_{fundCode}.html'
    if (CONFIG['useCache'] and os.path.isfile(filePath)):
        return False
    headers = {
        'Referer': f'http://fund.eastmoney.com/{fundCode}.html',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
    }
    requests_info = requests.get(f'http://fundf10.eastmoney.com/jjfl_{fundCode}.html', headers=headers)
    if requests_info.status_code == 200:
        html_bytes = requests_info.content
        html_str = html_bytes.decode()
        with open(filePath, 'w') as f:
            f.write(html_str)
    else:
        print(f'jjfl_-{requests_info.status_code}')
    return True


def getFloat(syl_1n):
    try:
        ret = float(syl_1n)
        return ret
    except Exception as e:
        return 0.0


# 分析数据
timeformat = lambda x: time.strftime("%Y-%m-%d", time.localtime(x / 1e3))
all_data_base = {}
all_data = {}
config_key = 'liquor_drink'  # liquor_drink
for item in CONFIG[config_key]:
    fundCode = item['code']
    print(f'downloading... {fundCode}')
    downed = downloadJson(fundCode)
    downed = downloadHtml(fundCode) or downed
    if (downloadJs(fundCode) or downed):
        time.sleep(2 * random.random())

    # 基本信息
    with open(f'{PATH_CACHE}/{fundCode}.js', 'r', encoding='utf8') as f:
        data = f.read()
        # print(data)
        # exit()
        # /*近一年收益率*/
        syl_1n = re.search(r'syl_1n\s?=\s?"([^\s]*)"', data).group(1)
        # /*近6月收益率*/
        syl_6y = re.search(r'syl_6y\s?=\s?"([^\s]*)"', data).group(1)
        # /*近三月收益率*/
        syl_3y = re.search(r'syl_3y\s?=\s?"([^\s]*)"', data).group(1)
        # /*近一月收益率*/
        syl_1y = re.search(r'syl_1y\s?=\s?"([^\s]*)"', data).group(1)
        # /*原费率*/
        fund_sourceRate = re.search(r'fund_sourceRate\s?=\s?"([^\s]*)"', data).group(1)
        # /*现费率*/
        fund_Rate = re.search(r'fund_Rate\s?=\s?"([^\s]*)"', data).group(1)
        # 名称
        fS_name = re.search(r'fS_name\s?=\s?"([^\s]*)"', data).group(1)
        # 规模
        Data_fluctuationScale = json.loads(re.search(r'Data_fluctuationScale\s?=\s?(\{[^\s]*\})', data).group(1))

        all_data_base[fS_name] = {}
        all_data_base[fS_name]['代码'] = fundCode
        all_data_base[fS_name]['近一年收益率'] = getFloat(syl_1n)
        all_data_base[fS_name]['近六月收益率'] = getFloat(syl_6y)
        all_data_base[fS_name]['近三月收益率'] = getFloat(syl_3y)
        all_data_base[fS_name]['近一月收益率'] = getFloat(syl_1y)
        all_data_base[fS_name]['买入费率'] = fund_sourceRate + '%'
        all_data_base[fS_name]['买入费率(优惠)'] = fund_Rate + '%'
        all_data_base[fS_name]['基金规模(亿元)'] = Data_fluctuationScale['series'][-1]['y']

    # 购买信息(费率表)
    with open(f'{PATH_CACHE}/jjfl_{fundCode}.html', 'r') as f:
        data = f.read()
        selector = lxml.html.fromstring(data)
        # 管理费率
        mg_rate = \
            selector.xpath('/html/body/div[1]/div[8]/div[3]/div[2]/div[3]/div/div[4]/div/table/tbody/tr/td[2]/text()')[
                0]
        all_data_base[fS_name]['管理费率'] = mg_rate
        # 托管费率
        mg_rate = \
            selector.xpath('/html/body/div[1]/div[8]/div[3]/div[2]/div[3]/div/div[4]/div/table/tbody/tr/td[4]/text()')[
                0]
        all_data_base[fS_name]['托管费率'] = mg_rate
        # 销售服务费率
        mg_rate = \
            selector.xpath('/html/body/div[1]/div[8]/div[3]/div[2]/div[3]/div/div[4]/div/table/tbody/tr/td[6]/text()')[
                0]
        all_data_base[fS_name]['销售服务费率'] = mg_rate
        # 赎回费率
        mg_rate = '--'
        try:
            mg_rate = selector.xpath('/html/body/div[1]/div[8]/div[3]/div[2]/div[3]/div/div[7]/div/table/tbody')[
                0].xpath('string(.)')
        except Exception as e:
            try:
                mg_rate = selector.xpath('/html/body/div[1]/div[8]/div[3]/div[2]/div[3]/div/div[6]/div/table/tbody')[
                    0].xpath('string(.)')
            except Exception as e:
                pass
        all_data_base[fS_name]['赎回费率'] = mg_rate

    # 处理收益
    with open(f'{PATH_CACHE}/{fundCode}.json', 'r') as f:
        data = json.load(f)['Data'][0]['data']
        arr1 = np.array(data)
        indexs = [timeformat(x) for x in arr1[:, 0:1].ravel()]
        values = [x for x in arr1[:, 1:2].ravel()]
        count = 0
        for index in indexs:
            if ((fundCode in all_data) == False):
                all_data[fundCode] = {}
            all_data[fundCode][index] = values[count]
            count = count + 1

# 保存数据
fig, axes = plt.subplots(2, 1)
# 处理基本信息
df2 = DataFrame(all_data_base)
print(df2)

df2.stack().unstack(0).to_excel(f'{DATA_PATH}/stock_fund/{config_key}_{time.time()}.xlsx', sheet_name='out')
df2.iloc[1:5, :].plot.barh(ax=axes[0], grid=True, fontsize=25)

# 处理收益
df = DataFrame(all_data).sort_index().fillna(method='ffill')
print(df)
df.plot(ax=axes[1], grid=True, fontsize=25)

fig.set_size_inches(20, 20)
fig.savefig(f'{DATA_PATH}/stock_fund/{config_key}_{time.time()}.png')

# https://www.zhihu.com/question/25404709 matplotlib图例中文乱码
