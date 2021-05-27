# coding: utf-8
# 按星期统计基金涨跌次数、给定投参考

import json
import matplotlib.pyplot as plt
import os
import urllib.request
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time
import random
import sys

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
PATH_WEEKDAY = DATA_PATH + 'stock_fund/weekday/'

# 加载配置
CONFIG = {}
with open(DATA_PATH + 'config/fund_config.json', 'r', encoding='utf8') as f:
    CONFIG = json.load(f)


# 获取单个fund历史净值数据
def fund_pages_data(fund_code, total_page=74, curr_page=1):
    open(f'{PATH_WEEKDAY}{fund_code}.txt', 'w').close()
    prev_page = curr_page

    # 78为天天基金网基金的历史数据总页数+1
    for i in range(curr_page, total_page+1):
        i = str(i)
        fund_code = str(fund_code)
        res = urllib.request.urlopen(
            "http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&per=20&sdate=&edate=&rt=0.7518869023828249&page=" + i + "&code=" + fund_code)
        html_content = res.read()
        soup = BeautifulSoup(html_content, "html.parser", from_encoding="utf-8")
        trs = soup.find_all('tr')
        i = 0
        for tr in trs:
            if i == 0:
                i += 1
                continue
            info_date = re.search(r'\d+-\d+-\d+', str(tr))
            info_net_value = re.search(r"\d+\.\d+", str(tr))
            info_rate = re.search(r"(|-)\d+\.\d+%", str(tr))
            if info_date is None and info_rate is None:
                if prev_page == i - 1:
                    print('连续出现2次None，退出page向下执行')
                    break
                prev_page = i

            if info_date is None or info_rate is None:
                print('code: {}, page: {}, date: {} is None!'.format(fund_code, i, info_date))
                continue

            fund_info = info_date.group() + "\t" + info_net_value.group() + "\t" + info_rate.group()
            with open(f'{PATH_WEEKDAY}{fund_code}.txt', "a+", encoding='utf-8') as fd:
                fd.write(fund_info + "\n")

        print('code: {}, page: {} data done!'.format(fund_code, i))
        time.sleep(2 * random.random())


# 获取所有fund历史净值
def get_all_data(key='top'):
    for item in CONFIG[key]:
        fund_pages_data(item['code'])


# 按星期汇总
def weekday_sum(fund_code):
    count = {}
    with open(f'{PATH_WEEKDAY}{fund_code}.txt', 'r') as file:
        lines = file.readlines()
        first_line = lines[0]  # 取第一行
        end_date = first_line.strip().split("\t")[0]
        last_line = lines[-1]  # 取最后一行
        start_date = last_line.strip().split("\t")[0]
        for line in lines:
            item = line.strip().split("\t")
            weekday = int(datetime.strptime(item[0], '%Y-%m-%d').weekday())
            # 周末过滤
            if weekday >= 5:
                continue

            if weekday not in count.keys():
                count[weekday] = {'up': 0, 'down': 0}

            rate = float(item[2].split("%")[0])
            if rate > 0:
                count[weekday]['up'] += 1
            else:
                count[weekday]['down'] += 1

    return {'start': start_date, 'end': end_date, 'total': count}


# 绘制单个柱状图
def draw_one_zhu(fund_code):
    data = weekday_sum(fund_code)
    total = data['total']
    if not total:
        print('{} data is empty!'.format(fund_code))
        sys.exit(0)

    # 排序
    total_asc = sorted(total.items(), key=lambda item: item[0])

    up_data = []
    down_data = []
    for k, val in total_asc:
        up_data.append(val['up'])
        down_data.append(val['down'])

    # 添加图形属性
    # plt.xlabel('星期')
    plt.ylabel('次数')
    plt.title(f'{data["start"]}至{data["end"]} {fund_code}涨跌分布图', fontsize=14, pad=10, fontweight='heavy', color='blue')
    x = list(range(len(up_data)))

    total_width, n = 0.8, 3
    width = total_width / n

    # x轴，数据，宽度，label
    up_bar = plt.bar(x, up_data, width=width, label='涨', color='red')

    for i in range(len(x)):
        x[i] = x[i] + width
    down_bar = plt.bar(x, down_data, width=width, label='跌', color='green')

    # 开始绘制x轴的数据
    name_list = ['周一', '周二', '周三', '周四', '周五']  # x轴标签
    index = range(len(name_list))
    plt.xticks(index, name_list, size=14)  # 绘制x轴的标签

    # 开始绘制y轴的数据
    # plt.yticks(range(minytick, maxytick, 200), size=20)  # y坐标

    # 柱形图顶端数值显示
    for bar1, bar2 in zip(up_bar, down_bar):
        y1 = bar1.get_height()
        x1 = bar1.get_x()
        plt.text(x1 + 0.01, y1, str(y1), va='bottom', fontsize=12, color="r")  # 0.15为偏移值，可以自己调整，正好在柱形图顶部正中

        y2 = bar2.get_height()
        x2 = bar2.get_x()
        plt.text(x2, y2, str(y2), va='bottom', color="g")  # 0.15为偏移值，可以自己调整，正好在柱形图顶部正中

    plt.legend()
    plt.savefig(f'{PATH_WEEKDAY}{fund_code}.png')
    # plt.show()
    plt.close()


# 批量绘图
def draw_all_zhu(key='top'):
    for item in CONFIG[key]:
        draw_one_zhu(item['code'])
        print('code: {} is draw done!'.format(item['code']))


# 分析数据
def main():
    fund_code = 161725
    # http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&per=20&sdate=&edate=&rt=0.7518869023828249&page=24&code=161725
    total_page = 74
    # fund_pages_data(fund_code, total_page)
    # get_all_data()
    draw_one_zhu(fund_code)
    # draw_all_zhu()


if __name__ == '__main__':
    main()
