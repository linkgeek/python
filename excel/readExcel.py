import pandas as pd
import os

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
path = '../data/config.xls'
# pd.read_excel('例子'.decode('utf-8))
data = pd.read_excel(path, sheet_name="Sheet1")
valData = data['value']
print(valData)

for col, idx in range(valData):
    print(idx, col)
exit()

print('显示表格的属性:', data.shape)  # 打印显示表格的属性，几行几列
print('显示表格的列名:', data.columns)  # 打印显示表格有哪些列名

# head() 默认显示前5行，可在括号内填写要显示的条数
print('显示表格前三行:', data.head(3))

print('--------------------------华丽的分割线----------------------------')
# tail() 默认显示后5行，可在括号内填写要显示的条数
print('显示表格后五行:', data.tail())
