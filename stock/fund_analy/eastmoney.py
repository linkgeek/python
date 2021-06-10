import requests
from bs4 import BeautifulSoup
import re
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# 指定默认字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['font.family'] = 'sans-serif'
# 解决负号'-'显示为方块的问题
matplotlib.rcParams['axes.unicode_minus'] = False

# 绝对路径
work_dir = os.path.dirname(os.path.abspath(__file__))
# 把当前路径切换到文件所在的路径
os.chdir(work_dir)

dir_path = '../../'
path_images = dir_path + 'images/'

sys.path.append(dir_path)
from lib.eastmoney import EastMoney


# 基金历史净值数据
# https://zhuanlan.zhihu.com/p/58264923
def analyse_history_rise(code=161725):
    em = EastMoney()
    data = em.get_rise_record(code=code, sdate='2018-01-01', edate='2021-06-07', per=49)
    print(data)
    exit()
    # 修改数据类型
    data['净值日期'] = pd.to_datetime(data['净值日期'], format='%Y/%m/%d')
    data['单位净值'] = data['单位净值'].astype(float)
    data['累计净值'] = data['累计净值'].astype(float)
    data['日增长率'] = data['日增长率'].str.strip('%').astype(float)
    # 按照日期升序排序并重建索引
    data = data.sort_values(by='净值日期', axis=0, ascending=True).reset_index(drop=True)
    print(data)

    # 获取净值日期、单位净值、累计净值、日增长率等数据并
    net_value_date = data['净值日期']
    net_asset_value = data['单位净值']
    accumulative_net_value = data['累计净值']
    daily_growth_rate = data['日增长率']

    # 作基金净值图
    fig = plt.figure()
    # 坐标轴1
    ax1 = fig.add_subplot(111)
    ax1.plot(net_value_date, net_asset_value)
    ax1.plot(net_value_date, accumulative_net_value)
    ax1.set_ylabel('净值数据')
    ax1.set_xlabel('日期')
    plt.legend(loc='upper left')
    # 坐标轴2
    ax2 = ax1.twinx()
    ax2.plot(net_value_date, daily_growth_rate, 'r')
    ax2.set_ylabel('日增长率（%）')
    plt.legend(loc='upper right')
    plt.title('基金净值数据')
    plt.savefig(f'{path_images}em-{code}历史净值数据.png')
    plt.show()

    # 绘制分红配送信息图
    bonus = accumulative_net_value - net_asset_value
    plt.figure()
    plt.plot(net_value_date, bonus)
    plt.xlabel('日期')
    plt.ylabel('累计净值-单位净值')
    plt.title('基金分红信息')
    plt.show()

    # 日增长率分析
    print('日增长率缺失：', sum(np.isnan(daily_growth_rate)))
    print('日增长率为正的天数：', sum(daily_growth_rate > 0))
    print('日增长率为负(包含0)的天数：', sum(daily_growth_rate <= 0))


def main():
    analyse_history_rise()


if __name__ == '__main__':
    main()
