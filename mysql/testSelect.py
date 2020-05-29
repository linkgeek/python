# encoding=utf8
from helper.MysqlHelper import *

sql = 'select * from student where id=%s'
id = input("请输入id：")
params = [id]

mysqlHelper = MysqlHelper('127.0.0.1', 'root', 'root', 'python')
one = mysqlHelper.get_one(sql, params)
print(one)