# coding: utf-8
# 分析基金 基金对比 基金业绩

import random
import requests
import time
from pandas import DataFrame
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

# 显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决负号“-”显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

DATA_PATH = '../../data/'
PATH_CACHE = DATA_PATH + 'fund_cache'

# 加载配置
CONFIG = {}
with open(DATA_PATH + 'config/fund_config.json', 'r', encoding='utf8') as f:
    CONFIG = json.load(f)


# 获取json数据
def download_json(fund_code):
    file_path = f'{PATH_CACHE}/{fund_code}.json'
    if CONFIG['useCache'] and os.path.isfile(file_path):
        return False

    requests_url = 'http://api.fund.eastmoney.com/pinzhong/LJSYLZS'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        'Accept': 'application/json',
        'Referer': f'http://fund.eastmoney.com/{fund_code}.html',
    }
    params = {
        'fundCode': f'{fund_code}',
        'indexcode': '000300',
        'type': 'try',
    }
    requests_page = requests.get(requests_url, headers=headers, params=params)
    if requests_page.status_code == 200:
        with open(file_path, 'w', encoding='utf8') as fp:
            json.dump(requests_page.json(), fp)
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


# 获取js
def download_js(fund_code):
    file_path = f'{PATH_CACHE}/{fund_code}.js'
    if CONFIG['useCache'] and os.path.isfile(file_path):
        return False
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
    }
    requests_info = requests.get(f'http://fund.eastmoney.com/pingzhongdata/{fund_code}.js', headers=headers)
    if requests_info.status_code == 200:
        html_bytes = requests_info.content
        html_str = html_bytes.decode()
        with open(file_path, 'w', encoding='utf8') as fp:
            fp.write(html_str)
    else:
        print(f'requests_info-{requests_info.status_code}')
    return True


# 获取html
def download_html(fund_code):
    file_path = f'{PATH_CACHE}/jjfl_{fund_code}.html'
    if CONFIG['useCache'] and os.path.isfile(file_path):
        return False
    headers = {
        'Referer': f'http://fund.eastmoney.com/{fund_code}.html',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
    }
    requests_info = requests.get(f'http://fundf10.eastmoney.com/jjfl_{fund_code}.html', headers=headers)
    if requests_info.status_code == 200:
        html_bytes = requests_info.content
        html_str = html_bytes.decode()
        with open(file_path, 'w') as fp:
            fp.write(html_str)
    else:
        print(f'jjfl_-{requests_info.status_code}')
    return True


# float格式化
def get_float(syl_1n):
    try:
        return float(syl_1n)
    except Exception as e:
        return 0.0


def get_data(config_key):
    time_format = lambda x: time.strftime("%Y-%m-%d", time.localtime(x / 1e3))
    all_data_base = {}
    all_data = {}
    config_key = 'liquor_drink'  # liquor_drink | medical_care | new_energy | bdt
    for item in CONFIG[config_key]:
        fund_code = item['code']
        print(f'downloading... {fund_code}')
        downed = download_json(fund_code)
        downed = download_html(fund_code) or downed
        if download_js(fund_code) or downed:
            time.sleep(2 * random.random())

        # 基本信息
        with open(f'{PATH_CACHE}/{fund_code}.js', 'r', encoding='utf8') as fp:
            data = fp.read()
            # /*近一年收益率*/
            syl_1n = re.search(r'syl_1n\s?=\s?"([^\s]*)"', data).group(1)
            # /*近6月收益率*/
            syl_6y = re.search(r'syl_6y\s?=\s?"([^\s]*)"', data).group(1)
            # /*近三月收益率*/
            syl_3y = re.search(r'syl_3y\s?=\s?"([^\s]*)"', data).group(1)
            # /*近一月收益率*/
            syl_1y = re.search(r'syl_1y\s?=\s?"([^\s]*)"', data).group(1)
            # /*原费率*/
            fund_source_rate = re.search(r'fund_sourceRate\s?=\s?"([^\s]*)"', data).group(1)
            # /*现费率*/
            fund_rate = re.search(r'fund_Rate\s?=\s?"([^\s]*)"', data).group(1)
            # 名称
            fs_name = re.search(r'fS_name\s?=\s?"([^\s]*)"', data).group(1)
            # 规模
            data_fluctuation_scale = json.loads(re.search(r'Data_fluctuationScale\s?=\s?(\{[^\s]*\})', data).group(1))

            all_data_base[fs_name] = {}
            all_data_base[fs_name]['代码'] = fund_code
            all_data_base[fs_name]['近一年收益率'] = get_float(syl_1n)
            all_data_base[fs_name]['近六月收益率'] = get_float(syl_6y)
            all_data_base[fs_name]['近三月收益率'] = get_float(syl_3y)
            all_data_base[fs_name]['近一月收益率'] = get_float(syl_1y)
            all_data_base[fs_name]['买入费率'] = fund_source_rate + '%'
            all_data_base[fs_name]['买入费率(优惠)'] = fund_rate + '%'
            if len(data_fluctuation_scale['series']) == 0:
                fund_size = '未知'
            else:
                fund_size = data_fluctuation_scale['series'][-1]['y']
            all_data_base[fs_name]['基金规模(亿元)'] = fund_size

        # 购买信息(费率表)
        with open(f'{PATH_CACHE}/jjfl_{fund_code}.html', 'r') as fp:
            data = fp.read()
            selector = lxml.html.fromstring(data)
            # 管理费率
            mg_rate = \
                selector.xpath(
                    '/html/body/div[1]/div[8]/div[3]/div[2]/div[3]/div/div[4]/div/table/tbody/tr/td[2]/text()')[
                    0]
            all_data_base[fs_name]['管理费率'] = mg_rate
            # 托管费率
            mg_rate = \
                selector.xpath(
                    '/html/body/div[1]/div[8]/div[3]/div[2]/div[3]/div/div[4]/div/table/tbody/tr/td[4]/text()')[
                    0]
            all_data_base[fs_name]['托管费率'] = mg_rate
            # 销售服务费率
            mg_rate = \
                selector.xpath(
                    '/html/body/div[1]/div[8]/div[3]/div[2]/div[3]/div/div[4]/div/table/tbody/tr/td[6]/text()')[
                    0]
            all_data_base[fs_name]['销售服务费率'] = mg_rate
            # 赎回费率
            mg_rate = '--'
            try:
                mg_rate = selector.xpath('/html/body/div[1]/div[8]/div[3]/div[2]/div[3]/div/div[7]/div/table/tbody')[
                    0].xpath('string(.)')
            except Exception as e:
                try:
                    mg_rate = \
                        selector.xpath('/html/body/div[1]/div[8]/div[3]/div[2]/div[3]/div/div[6]/div/table/tbody')[
                            0].xpath('string(.)')
                except Exception as e:
                    pass
            all_data_base[fs_name]['赎回费率'] = mg_rate

        # 处理收益
        with open(f'{PATH_CACHE}/{fund_code}.json', 'r') as fp:
            data = json.load(fp)['Data'][0]['data']
            arr1 = np.array(data)
            index_arr = [time_format(x) for x in arr1[:, 0:1].ravel()]
            values = [x for x in arr1[:, 1:2].ravel()]
            count = 0
            for index in index_arr:
                if not (fund_code in all_data):
                    all_data[fund_code] = {}
                all_data[fund_code][index] = values[count]
                count = count + 1

    return all_data_base, all_data


def gen_xls_pic(config_key):
    all_data_base, all_data = get_data(config_key)
    # print(all_data_base, all_data)
    # exit()

    # 保存数据
    fig, axes = plt.subplots(2, 1)
    # 处理基本信息
    df2 = DataFrame(all_data_base)
    print(df2)
    # exit()

    # df.stack() 列索引→行索引    df.unstack() 行索引→列索引
    df3 = df2.stack().unstack(0)
    color_col_title = ['近一年收益率', '近六月收益率', '近三月收益率', '近一月收益率']
    df3.style.highlight_max(subset=color_col_title, color='red', axis=0).to_excel(
        f'{DATA_PATH}/stock_fund/{config_key}_{time.strftime("%Y%m%d%H", time.localtime())}.xlsx', sheet_name='out')
    df3.iloc[1:5, :].plot.barh(ax=axes[0], grid=True, fontsize=25)

    # 处理收益
    df = DataFrame(all_data).sort_index().fillna(method='ffill')
    print(df)
    df.plot(ax=axes[1], grid=True, fontsize=25)

    fig.set_size_inches(20, 20)
    fig.savefig(f'{DATA_PATH}/stock_fund/{config_key}_{time.strftime("%Y%m%d%H", time.localtime())}.png')


# 分析数据
def main():
    config_key = 'liquor_drink'  # liquor_drink medical_care new_energy
    gen_xls_pic(config_key)


if __name__ == '__main__':
    main()
