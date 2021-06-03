#!/usr/bin/python
# -*- coding: UTF-8 -*-
# https://mp.weixin.qq.com/s?__biz=MzU5NjM4MDY1Mw==&mid=2247489794&idx=1&sn=5e04990e875970602f774fa6ff994952&chksm=fe62c780c9154e965758c6b316bd05b7c016f9fe5cac2021b54a04614e3b023aa64a21b01a60&cur_album_id=1575641054601674754&scene=190#rd

import pymysql as pmq
import os
import sys

# 绝对路径
work_dir = os.path.dirname(os.path.abspath(__file__))
# 把当前路径切换到文件所在的路径
os.chdir(work_dir)

sys.path.append('../')
from api.mmysql import Mmysqli

# 接口
mr = Mmysqli('192.168.7.26', 'root', 'sdf*2018', 'giant_player')
sql = 'select * from t_player where playerID in (4320009, 4320462)'
data = mr.get_all(sql, {})
print(data)
print('--------------------------华丽的分割线----------------------------')

# connect(ip.user,password,dbname)
con = pmq.connect('192.168.7.26', 'root', 'sdf*2018', 'giant_player')

# 操作游标
cur = con.cursor()


# 创建 movie 表
movie_sql = '''
        create table movie(
            id int AUTO_INCREMENT  primary key not null,
            title varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci  not null,
            url varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci  not null,
            rate float  not null
        )
'''
# 执行sql语句
cur.execute(movie_sql)
# 提交到数据库执行
con.commit()

print('--------------------------华丽的分割线----------------------------')

