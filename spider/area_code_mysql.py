# coding=utf-8
# -*- coding: utf-8 -*-


import urllib.request
import time

from bs4 import BeautifulSoup

import pymysql

# 当成是mysqldb一样使用，当然也可以不写这句，那就按照pymysql的方式
pymysql.install_as_MySQLdb()

user = 'root'
pas = 'admin123'
db = 'test'


def execSql(sql):
    conn = pymysql.connect(host='localhost', user=user, passwd=pas, db=db, port=3306, charset='utf8')
    cur = conn.cursor()  # 获取一个游标
    try:
        # print(sql)
        cur.execute(sql)

        conn.commit()
    except:
        conn.rollback()
        conn.close()
    # data=cur.fetchall()
    # cur.close()#关闭游标
    # conn.close()#释放数据库资源


def getHTMLText(url):
    maxTryNum = 20
    for tries in range(maxTryNum):
        try:
            # kv = {"user-agent": "Mizilla/5.0"}
            response = urllib.request.urlopen(url, timeout=30000).read().decode('gbk')
            return response
        except:
            if tries < (maxTryNum - 1):
                continue
            else:
                print("Has tried %d times to access url %s, all failed!" % (maxTryNum, url))
                break


indexs = 'index.html'
url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/'

txt = getHTMLText(url + indexs)  # urllib.request.urlopen(url + indexs).read().decode('gbk')
soup = BeautifulSoup(txt, 'html.parser')
lista = soup.find_all('a')
lista.pop()
flag = 0
dd = ''
for idx, a in enumerate(lista):
    id = flag = flag + idx + 1
    dd = code = a['href'][0:2]
    name = a.text
    level = '0'
    pid = id

    sql = "insert into city (id,code,name,level,pid)values('" + str(
        id) + "','" + code + "','" + name + "','" + level + "','" + str(pid) + "');"
    execSql(sql)
    print("========" + a['href'][0:2] + "," + a.text + "========")
    time.sleep(2)
    txt = getHTMLText(url + a['href'])  # urllib.request.urlopen(url + a['href'],timeout=30000).read().decode('gbk')
    soup = BeautifulSoup(txt, 'html.parser')
    listb = soup.find_all('a')
    listb.pop()
    bb = {}
    l = len(listb)
    # print("----->>>>> "+str(l/2)+" <<<<<<------")
    strName = ''

    pida = id
    for i in range(0, l - 1):
        time.sleep(3)
        if (listb[i].text == strName):
            continue

        strIndex = listb[i]['href']
        code = listb[i].text
        strName = name = listb[i + 1].text

        ida = flag = flag + 1
        level = '1'
        pid = pida

        sql = "insert into city (id,code,name,level,pid)values('" + str(
            ida) + "','" + code + "','" + name + "','" + level + "','" + str(pid) + "');"
        execSql(sql)
        print(strIndex + "," + code + "," + name)

        ctxt = getHTMLText(url + strIndex)  # urllib.request.urlopen(url + strIndex,timeout=30000).read().decode('gbk')
        soup = BeautifulSoup(ctxt, 'html.parser')
        listc = soup.find_all('a')
        listc.pop()
        lc = len(listc)
        # print("----->>>>> "+str(lc/2)+" <<<<<<------")
        cstrName = ''

        pidc = ida
        for c in range(0, lc - 1):
            time.sleep(3)
            if (listc[c].text == cstrName):
                continue

            strIndex = listc[c]['href']

            code = listc[c].text
            cstrName = name = listc[c + 1].text
            idc = flag = flag + 1
            level = '2'
            pid = pidc

            sql = "insert into city (id,code,name,level,pid)values('" + str(
                idc) + "','" + code + "','" + name + "','" + level + "','" + str(pid) + "');"
            execSql(sql)
            print("   >[" + code + "," + name + "]")

            dtxt = getHTMLText(
                url + '/' + dd + '/' + strIndex)  # urllib.request.urlopen(url +'/'+dd+'/'+ strIndex,timeout=30000).read().decode('gbk')
            soup = BeautifulSoup(dtxt, 'html.parser')
            listd = soup.find_all('a')
            listd.pop()

            ld = len(listd)
            print("----->>>>> " + str(ld / 2) + " <<<<<<------")
            dstrName = ''

            pidd = idc
            for d in range(0, ld - 1):
                if (listd[d].text == dstrName):
                    continue
                strIndex = listd[d]['href']
                code = listd[d].text
                dstrName = name = listd[d + 1].text
                idd = flag = flag + 1
                level = '3'
                pid = pidd

                sql = "insert into city (id,code,name,level,pid)values('" + str(
                    idd) + "','" + code + "','" + name + "','" + level + "','" + str(pid) + "');"
                execSql(sql)
                print("   ====[" + code + "," + name + "]====")
