# encoding=utf8
from lib.MysqlHelper import *

sql = 'update student set name=%s, gender=%s where id=%s'
id = input('请输入编号：')
name = input("请输入用户名：")
gender = input("请输入性别，1男，0女：")
params = [name, int(gender), id]

mysqlHelper = MysqlHelper('127.0.0.1', 'root', 'root', 'python')
count = mysqlHelper.update(sql, params)
if count == 1:
    print('ok')
else:
    print('error')