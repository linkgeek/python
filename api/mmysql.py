#!/usr/bin/python
# -*- coding: UTF-8 -*-
# https://mp.weixin.qq.com/s?__biz=MzU5NjM4MDY1Mw==&mid=2247489794&idx=1&sn=5e04990e875970602f774fa6ff994952&chksm=fe62c780c9154e965758c6b316bd05b7c016f9fe5cac2021b54a04614e3b023aa64a21b01a60&cur_album_id=1575641054601674754&scene=190#rd

import pymysql as pmq


# mysql类封装
class Mmysqli:
    conn = None
    cursor = None

    def __init__(self, host, user, password, db, port=3306, charset='utf8'):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset
        self.port = port

    def connect(self):
        try:
            self.conn = pmq.connect(host=self.host, user=self.user, password=self.password, db=self.db,
                                    charset=self.charset, port=self.port)
            # 操作游标
            self.cursor = self.conn.cursor()
        except Exception as e:
            print('mysql连接失败，错误信息%s' % e)

    # 创建表
    def create_table(self, sql=''):
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
        self.cursor.execute(movie_sql)
        # 提交到数据库执行
        self.conn.commit()

    # 获取单条数据
    def get_one(self, sql, params=()):
        result = None
        try:
            self.connect()
            self.cursor.execute(sql, params)
            result = self.cursor.fetchone()
            self.close()
        except Exception as e:
            print(e)
        return result

    #
    def get_all(self, sql, params=()):
        list_data = ()
        try:
            self.connect()
            self.cursor.execute(sql, params)
            list_data = self.cursor.fetchall()
            self.close()
        except Exception as e:
            print(e)
        return list_data

    # 关闭链接
    def close(self):
        self.cursor.close()
        self.conn.close()
