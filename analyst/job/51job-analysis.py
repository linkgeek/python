# -*- coding: utf-8 -*-
import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import operator
import os

# 绝对路径
work_dir = os.path.dirname(os.path.abspath(__file__))
# 把当前路径切换到文件所在的路径
os.chdir(work_dir)

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
# 岗位
title_list = []
# 城市
city_list = []
# 薪资分布
salary_list = []

job_csv = '../../data/csv/'

with open(f'{job_csv}爬虫工程师岗位薪资.csv', 'r', encoding='utf-8') as fp:
    reader = csv.reader(fp)
    for row in reader:
        # 岗位
        title_list.append(row[0])
        # 城市
        city_list.append(row[2][0:2])
        # 薪资分布
        salary = row[3].split("-")
        if (len(salary) == 2):
            try:
                salary = salary[1].replace("/月", "")
                if "万" in salary:
                    salary = salary.replace("万", "")
                    salary = int(salary)
                    salary = salary * 10000
                    salary_list.append(salary)
                if "千" in salary:
                    salary = salary.replace("千", "")
                    salary = int(salary)
                    salary = salary * 1000
                    salary_list.append(salary)
            except:
                pass


# -----------可视化1：爬虫岗位常用名称-------
def job_name():
    dict_x = {}
    for item in title_list:
        dict_x[item] = title_list.count(item)
    sorted_x = sorted(dict_x.items(), key=operator.itemgetter(1), reverse=True)
    k_list = []
    v_list = []
    for k, v in sorted_x[0:11]:
        k_list.append(k)
        v_list.append(v)
    plt.axes(aspect=1)
    plt.title(u'爬虫岗位常用名称')
    plt.pie(x=v_list, labels=k_list, autopct='%0f%%')
    plt.savefig(f"{job_csv}爬虫岗位常用名称.png", dpi=600)
    plt.show()


# ------------可视化2：爬虫岗位最多的城市----------
def job_city():
    dict_x = {}
    for item in city_list:
        dict_x[item] = city_list.count(item)
    sorted_x = sorted(dict_x.items(), key=operator.itemgetter(1), reverse=True)
    k_list = []
    v_list = []
    for k, v in sorted_x[0:11]:
        k_list.append(k)
        v_list.append(v)

    plt.bar(k_list, v_list, label='爬虫岗位最多的城市')
    plt.legend()
    plt.xlabel('城市')
    plt.ylabel('数量')
    plt.title(u'爬虫岗位最多的城市')
    plt.savefig(f"{job_csv}爬虫岗位最多的城市.png", dpi=600)
    plt.show()


# ------------可视化3：薪资分布情况----------
def salary_scatter():
    dict_x = {}
    for item in salary_list:
        dict_x[item] = salary_list.count(item)
    sorted_x = sorted(dict_x.items(), key=operator.itemgetter(1), reverse=True)
    k_list = []
    v_list = []
    for k, v in sorted_x[0:15]:
        k_list.append(k)
        v_list.append(v)
    plt.axes(aspect=1)
    plt.title(u'薪资分布情况')
    plt.pie(x=v_list, labels=k_list, autopct='%0f%%')
    plt.savefig(f"{job_csv}薪资分布情况.png", dpi=600)
    plt.show()


# 频率分布
def rate_scatter():
    data = pd.DataFrame({"value": salary_list})
    cats1 = pd.cut(data['value'].values, bins=[8000, 10000, 20000, 30000, 50000, data['value'].max() + 1])
    pinshu = cats1.value_counts()
    pinshu_df = pd.DataFrame(pinshu, columns=['频数'])
    pinshu_df['频率f'] = pinshu_df / pinshu_df['频数'].sum()
    pinshu_df['频率%'] = pinshu_df['频率f'].map(lambda x: '%.2f%%' % (x * 100))
    pinshu_df['累计频率f'] = pinshu_df['频率f'].cumsum()
    pinshu_df['累计频率%'] = pinshu_df['累计频率f'].map(lambda x: '%.4f%%' % (x * 100))
    print(pinshu_df)


salary_scatter()
