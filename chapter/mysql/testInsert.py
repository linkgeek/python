# encoding=utf8
from lib.MysqlHelper import *

sql = 'insert into student(name, gender) values(%s, %s)'
name = input("请输入用户名：")
gender = input("请输入性别，1男，0女：")
params = [name, bool(gender)]

mysqlHelper = MysqlHelper('127.0.0.1', 'root', 'root', 'python')
count = mysqlHelper.insert(sql, params)
if count == 1:
    print('ok')
else:
    print('error')