import pandas as pd
import os
import json

# 绝对路径
work_dir = os.path.dirname(os.path.abspath(__file__))
# 把当前路径切换到文件所在的路径
os.chdir(work_dir)

# io: 很明显, 是excel文件的路径+名字字符串
# sheet_name: 返回指定的sheet, 默认返回全表，多表['sheet1', 'sheet2']
# name: 如果没有表头, 可用此参数传入列表做表头
# header: 指定数据表的表头,默认值为0, 即将第一行作为表头
# index_col: 用作行索引的列编号或者列名，如果给定一个序列则有多个行索引。一般可以设定index_col=False指的是pandas不适用第一列作为行索引。
# usecols：读取指定的列, 也可以通过名字或索引值

# read_excel()用来读取excel文件，记得加文件后缀
path = '../data/对话记录1-2362.xls'
# pd.read_excel('例子'.decode('utf-8))
df = pd.read_excel(path, sheet_name='1-2362')

# 获取最大行，最大列
nrows = df.shape[0]
ncols = df.columns.size
# print('Max Rows: ' + str(nrows))
# print('Max Columns: ' + str(ncols))
# print('--------------------------华丽的分割线----------------------------')

# print('显示表格的属性:', df.shape)  # 打印显示表格的属性，几行几列
# print('显示表格的列名:', df.columns)  # 打印显示表格有哪些列名
# 显示列名，并显示列名的序号
# for iCol in range(ncols):
#     print(str(iCol) + ':' + df.columns[iCol])
# 列出特定行列，单元格的值
# print(df.iloc[0, 0])
cont = df.iloc[0, 12]
cont_list = cont.split("\n")
for i, item in enumerate(cont_list):
    if '访客>' in item:
        print(i, cont_list[i+1])
# print(cont)
# print('--------------------------华丽的分割线----------------------------')

# 查看某列内容
# sColumnName='fd1'
# print(df[sColumnName])
#
# # 查看第3列的内容，列的序号从0开始
# sColumnName = df.columns[2]
# print(df[sColumnName])
#
# # 查看某行的内容
# iRow = 1
# for iCol in range(ncols):
#     print(df.iloc[iRow, iCol])
#
# # 遍历逐行逐列
# for iRow in range(nrows):
#     for iCol in range(ncols):
#         print(df.iloc[iRow, iCol])

# head() 默认显示前5行，可在括号内填写要显示的条数
# print('显示表格前三行:', df.head(3))

# print('--------------------------华丽的分割线----------------------------')
# tail() 默认显示后5行，可在括号内填写要显示的条数
# print('显示表格后五行:', df.tail())

# test_data = []
# for i in df.index.values:  # 获取行号的索引，并对其进行遍历：
#     # 根据i来获取每一行指定的数据 并利用to_dict转成字典
#     row_data = df.ix[i, ['请求时间', '入口', '对话内容']].to_dict()
#     test_data.append(row_data)
# print("最终获取到的数据是：{0}".format(test_data))
