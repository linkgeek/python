# -*- coding: utf-8 -*-
"""
git: https://gitee.com/lyc96/fund-visualization/blob/master/main.py

近一月涨跌幅前10名
基金各个阶段涨跌幅
近30个交易日净值情况
"""

import requests
from lxml import etree
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.charts import Bar
from pyecharts.charts import Pie
import json
import os

# 绝对路径
work_dir = os.path.dirname(os.path.abspath(__file__))
# 把当前路径切换到文件所在的路径
os.chdir(work_dir)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0', }
fund_path = '../../data/html/'

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
        .render(fund_path + str(picname) + ".html")
    )


# 柱形图
def bars(name, dict_values):
    # 链式调用
    c = (
        Bar(
            init_opts=opts.InitOpts(  # 初始配置项
                theme=ThemeType.MACARONS,
                animation_opts=opts.AnimationOpts(
                    animation_delay=1000, animation_easing="cubicOut"  # 初始动画延迟和缓动效果
                ))
        )
            .add_xaxis(xaxis_data=name)  # x轴
            .add_yaxis(series_name="股票型", yaxis_data=dict_values['股票型'])  # y轴
            .add_yaxis(series_name="混合型", yaxis_data=dict_values['混合型'])  # y轴
            .add_yaxis(series_name="债券型", yaxis_data=dict_values['债券型'])  # y轴
            .add_yaxis(series_name="指数型", yaxis_data=dict_values['指数型'])  # y轴
            .add_yaxis(series_name="QDII型", yaxis_data=dict_values['QDII型'])  # y轴
            .set_global_opts(
            title_opts=opts.TitleOpts(title='涨跌幅', subtitle='xxx绘制',  # 标题配置和调整位置
                                      title_textstyle_opts=opts.TextStyleOpts(
                                          font_family='SimHei', font_size=25, font_weight='bold', color='red',
                                      ), pos_left="90%", pos_top="10",
                                      ),
            xaxis_opts=opts.AxisOpts(name='阶段', axislabel_opts=opts.LabelOpts(rotate=45)),
            # 设置x名称和Label rotate解决标签名字过长使用
            yaxis_opts=opts.AxisOpts(name='涨跌点'),

        )
            .render("基金各个阶段涨跌幅.html")
    )
    c.render()


# 拉伸图
def silder(name, value, tips):
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
            .add_xaxis(xaxis_data=name)
            .add_yaxis(tips, yaxis_data=value)
            .set_global_opts(
            title_opts=opts.TitleOpts(title=str(tips) + "近30个交易日净值情况"),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
        )
            .render(str(tips) + "近30个交易日净值情况.html")
    )


# 基金类型
dict_type = {"股票型": 1, "混合型": 3, "债券型": 2, "指数型": 5, "QDII型": 11}
# 时间
dict_time0 = {'近一周': '1w', '近一月': '1m', '近三月': '3m', '近六月': '6m', '近1年': '1y', '近2年': '2y', '近3年': '3y', '近5年': '5y'}
dict_time = {
    '1w': '近一周',
    '1m': '近一月',
    '3m': '近三月',
    '6m': '近六月',
    '1y': '近1年',
    '2y': '近2年',
    '3y': '近3年',
    '5y': '近5年'
}


# #分析1： 近一月涨跌幅前10名
def analysis1(time='1w'):
    for key in dict_type:
        url = "https://danjuanapp.com/djapi/v3/filter/fund?type=" + str(
            dict_type[key]) + "&order_by=" + time + "&size=10&page=1"
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        s = json.loads(res.text)
        s = s['data']['items']
        name = []
        value = []
        print('\n{}基金{}涨跌幅前10名'.format(key, dict_time[time]))
        print('--------------------------华丽的分割线----------------------------')
        for i in range(0, len(s)):
            print(s[i]['fd_name'] + ": " + s[i]['yield'])
            name.append(s[i]['fd_name'])
            value.append(s[i]['yield'])
        # 开始绘图
        pie(name, value, str(key) + "基金涨跌幅", "[" + str(key) + "]基金近一月涨跌幅前10名")


# 分析2： 基金各个阶段涨跌幅
def analysis2():
    name = ['近1周', '近1月', '近3月', '近6月', '近1年', '近3年', '近5年']
    # 五类基金
    dict_value = {}

    for key in dict_type:
        # 获取排名第一名基金代号
        url = "https://danjuanapp.com/djapi/v3/filter/fund?type=" + str(dict_type[key]) + "&order_by=1w&size=10&page=1"
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        s = json.loads(res.text)
        # 取第一名
        fd_code = s['data']['items'][0]['fd_code']

        #  获取排名第一名基金各个阶段情况
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
    print(name, dict_value)
    # exit()
    bars(name, dict_value)


# 分析3： 近30个交易日净值情况
def analysis3():
    for key in dict_type:
        #  获取排名第一名基金代号
        url = "https://danjuanapp.com/djapi/v3/filter/fund?type=" + str(
            dict_type[key]) + "&order_by=1w&size=10&page=1"
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        s = json.loads(res.text)
        # 取第一名
        fd_code = s['data']['items'][0]['fd_code']

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

        silder(name, value, key)


# name =['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']
# value=[34,42,12,37,76,11,13,53,42,23,43,64,67,22,41]
# 分析1： 近一月涨跌幅前10名
analysis1()

# 分析2：基金各个阶段涨跌幅
# analysis2()

# 分析3：近30个交易日净值情况
# analysis3()
