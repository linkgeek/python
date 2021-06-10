# -*- coding: utf-8 -*-
"""
git: https://gitee.com/lyc96/fund-visualization/blob/master/main.py

近一月涨跌幅前10名
基金各个阶段涨跌幅
近30个交易日净值情况
"""
import sys
import requests
from lxml import etree
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.charts import Bar
from pyecharts.charts import Pie
import matplotlib.pyplot as plt
from pandas import DataFrame

# 导入输出图片工具
from pyecharts.render import make_snapshot
# 使用snapshot-selenium 渲染图片
from snapshot_selenium import snapshot
import json
import os
import time

work_dir = os.path.dirname(os.path.abspath(__file__))
# 把当前路径切换到文件所在的路径
os.chdir(work_dir)

sys.path.append('../../')
from lib.helper import Helper

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0', }
data_path = '../../data/'
fund_path = data_path + 'image/'
path_html = data_path + 'html/'


# 饼状图
def pie(name, value, picname, tips):
    c = (
        Pie(init_opts=opts.InitOpts(width="1000px", height="500px", theme=ThemeType.CHALK))
            .add("", [list(z) for z in zip(name, value)], center=["40%", "50%"])
            .set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple"])  # 设置颜色
            .set_global_opts(
            title_opts=opts.TitleOpts(title="" + str(tips)),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="75%", orient="vertical"),  # 调整图例位置
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        # .render(fund_path + str(picname) + ".png")
    )
    # 输出保存为图片
    make_snapshot(snapshot, c.render(), fund_path + str(picname) + ".png")


# 柱形图
def bars(name, dict_values, title):
    # 链式调用
    c = (
        Bar(
            init_opts=opts.InitOpts(
                theme=ThemeType.MACARONS,
                animation_opts=opts.AnimationOpts(
                    animation_delay=1000, animation_easing="cubicOut"
                )
            )
        )
            .add_xaxis(xaxis_data=name)  # x轴
            .add_yaxis(series_name="股票型", y_axis=dict_values['股票型'])  # y轴
            .add_yaxis(series_name="混合型", y_axis=dict_values['混合型'])
            .add_yaxis(series_name="债券型", y_axis=dict_values['债券型'])
            .add_yaxis(series_name="指数型", y_axis=dict_values['指数型'])
            .add_yaxis(series_name="QDII型", y_axis=dict_values['QDII型'])
            .set_global_opts(
            title_opts=opts.TitleOpts(title=title, subtitle='',
                                      title_textstyle_opts=opts.TextStyleOpts(
                                          font_family='SimHei', font_size=20, font_weight='bold', color='red',
                                      ), pos_left="28%", pos_top="10",
                                      ),
            xaxis_opts=opts.AxisOpts(name='阶段', axislabel_opts=opts.LabelOpts(rotate=45)),
            # 图例设置
            legend_opts=opts.LegendOpts(
                pos_left='right',  # 图例放置的位置，分上下左右，可用左右中表示，也可用百分比表示
                pos_top='center',
                orient='vertical',  # horizontal、vertical #图例放置的方式 横着放or竖着放
                textstyle_opts=opts.TextStyleOpts(
                    font_size=12,
                    font_family='Times New Roman',
                ),
            ),
            # 设置x名称和Label rotate解决标签名字过长使用
            yaxis_opts=opts.AxisOpts(name='涨跌点'),

        )
            .render(path_html + "各类基金中第一名基金各个阶段的涨跌幅.html")
    )


# 拉伸图
def silder(name, value, tips):
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
            .add_xaxis(xaxis_data=name)
            .add_yaxis(tips, y_axis=value)
            .set_global_opts(
            title_opts=opts.TitleOpts(title=str(tips) + "近30个交易日净值情况"),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
        )
            .render(path_html + str(tips) + "近30个交易日净值情况.html")
    )


# 基金类型
dict_type = {"股票型": 1, "混合型": 3, "债券型": 2, "指数型": 5, "QDII型": 11}
# 时间
dict_time = {'1w': '近1周', '1m': '近1月', '3m': '近3月', '6m': '近6月', '1y': '近1年', '2y': '近2年', '3y': '近3年', '5y': '近5年'}

# 加载config
CONFIG = {}
with open(f'{data_path}config/fund_config.json', 'r', encoding='utf8') as f:
    CONFIG = json.load(f)


# 分析1：各个阶段涨跌幅前10名
def analysis1():
    for f_zh, f_type in dict_type.items():
        for t_en, t_zh in dict_time.items():
            url = "https://danjuanapp.com/djapi/v3/filter/fund?type=" + str(
                f_type) + "&order_by=" + t_en + "&size=10&page=1"
            res = requests.get(url, headers=headers)
            res.encoding = 'utf-8'
            s = json.loads(res.text)
            s = s['data']['items']
            name = []
            value = []
            print('\n{}基金{}涨跌幅前10名'.format(f_zh, t_zh))
            print('--------------------------华丽的分割线----------------------------')
            for i in range(0, len(s)):
                print(s[i]['fd_name'] + ": " + s[i]['yield'])
                code = s[i]['fd_code']
                name.append(s[i]['fd_name'] + "\n" + code)
                value.append(s[i]['yield'])
            # 开始绘图
            title = f'{f_zh}基金{t_zh}涨跌幅前10名'
            pie(name, value, title, title)


# 分析2：获取各类基金某阶段中第一名基金的各个阶段的涨跌幅情况
def analysis2(time='1w'):
    name = ['近1周', '近1月', '近3月', '近6月', '近1年', '近3年', '近5年']
    # 五类基金
    dict_value = {}
    code_value = []
    title = dict_time[time] + "第一名基金的各个阶段的涨跌幅情况"

    for key in dict_type:
        # 获取排名第一名基金代号
        url = "https://danjuanapp.com/djapi/v3/filter/fund?type=" + str(
            dict_type[key]) + "&order_by=" + time + "&size=10&page=1"
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        s = json.loads(res.text)
        # 取第一名
        fd_code = s['data']['items'][0]['fd_code']
        code_value.append(fd_code)

        # 获取排名第一名基金各个阶段涨幅情况
        fu_url = "https://danjuanapp.com/djapi/fund/derived/" + str(fd_code)
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
        # 添加到集合中
        dict_value[key] = values

    bars(name, dict_value, title)
    print(code_value)


# 分析3：多基金各个阶段的涨跌幅情况
def analysis3():
    all_data_base = {}
    config_key = 'top'  # liquor_drink medical_care new_energy
    data_map = {
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
    for obj in CONFIG[config_key]:
        code = obj['code']
        print(f'loading... {code}')
        cname = obj['name']
        fu_url = "https://danjuanapp.com/djapi/fund/derived/" + str(code)
        res = requests.get(fu_url, headers=headers)
        res.encoding = 'utf-8'
        s = json.loads(res.text)
        data = s['data']

        all_data_base[cname] = {}
        all_data_base[cname]['代码'] = code

        # 防止基金最长时间不够1年、2年、5年的情况报错，用0填充
        for key, val in data_map.items():
            try:
                if key == 'end_date':
                    all_data_base[cname][val] = data[key]
                else:
                    all_data_base[cname][val] = Helper.float_format(data[key])
            except:
                all_data_base[cname][val] = 0

    print(all_data_base)
    # exit()
    # 保存数据
    fig, axes = plt.subplots(2, 1)
    # 处理基本信息
    df2 = DataFrame(all_data_base)
    print(df2)

    df2.stack().unstack(0).to_excel(
        f'{data_path}/stock_fund/danjuan_{config_key}_{time.strftime("%Y%m%d%H%M", time.localtime())}.xlsx',
        sheet_name='out')
    df2.iloc[1:5, :].plot.barh(ax=axes[0], grid=True, fontsize=25)


# 分析3：获取各类基金某阶段中第一名基金的近30个交易日净值情况
def analysis4():
    code_value = []
    for key in dict_type:
        #  获取近1月排名第一名基金代号
        url = "https://danjuanapp.com/djapi/v3/filter/fund?type=" + str(
            dict_type[key]) + "&order_by=1w&size=10&page=1"
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        s = json.loads(res.text)
        # 取第一名
        fd_code = s['data']['items'][0]['fd_code']
        code_value.append(fd_code)

        #  获取排名第一名基金近30个交易日净值情况
        fu_url = "https://danjuanapp.com/djapi/fund/nav/history/" + str(fd_code) + "?size=30&page=1"
        res = requests.get(fu_url, headers=headers)
        res.encoding = 'utf-8'
        s = json.loads(res.text)
        data = s['data']['items']
        name = []
        value = []
        for k in range(0, len(data)):
            name.append(data[k]['date'])
            value.append(data[k]['nav'])

        tip = key + "[" + fd_code + "]"
        silder(name, value, tip)
    print(code_value)

# 分析1： 各类基金各个阶段的涨跌幅前10名
# analysis1()

# 分析2：各类基金第一名基金各个阶段的涨跌幅情况
# analysis2()

# 分析3：各基金各个阶段的涨跌幅情况
analysis3()

# 分析4：近30个交易日净值情况
# analysis4()
