#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import urllib.request
from urllib import request, parse
import urllib3
from lxml import etree
import xlwt
import time
import base64
import random
import re
import webbrowser as wb
import pandas as pd
import os

# 绝对路径
work_dir = os.path.dirname(os.path.abspath(__file__))
# 把当前路径切换到文件所在的路径
os.chdir(work_dir)

# 获取所有 li标签
xpath_items = '//div[@id="content"]/div/ul/li[position()>1][position()<last()]'
xpath_downbtn = '//div[@class="download"]/b//a/@href'
xpath_down = '//div[@class="download"]/b//a/@href'

# 对每个 li标签再提取
xpath_tip = './text()'
xpath_href = './a/@href'
xpath_title = './/text()'

urllib3.disable_warnings()
base_url = 'http://www.btxi.xyz/'
url = base_url + 'list.php?class=guochan'

headers = {
    'Host': 'www.btbw.xyz',
    # ':authority': 'www.btbw.xyz',
    # 'Cookie': 'cookie: _ga=GA1.1.1947293559.1621949576; cf_chl_prog=a10; cf_clearance=e44314b49a81e7dbafe935bdb5f74efe2acd8f6f-1621955693-0-250; _ga_Q3P79YL0DW=GS1.1.1621955693.2.0.1621955736.0',
    'cookie': '_ga=GA1.1.1947293559.1621949576; cf_clearance=e44314b49a81e7dbafe935bdb5f74efe2acd8f6f-1621955693-0-250; _ga_Q3P79YL0DW=GS1.1.1622037355.3.1.1622037391.0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',

    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
}


# 分页获取
def get_page_data(page, data, keywords, start_date):
    page_url = url + '&page=' + str(page)
    flag = False
    while True:
        try:
            r = requests.get(page_url, headers=headers, timeout=15, verify=False)
            r.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
        except requests.exceptions.RequestException as e:
            print(e)
            print('ConnectionError -- please wait 3 seconds')
            time.sleep(3)
        else:
            r.encoding = r.apparent_encoding
            dom = etree.HTML(r.text)
            r.close()

            # 获取每页所有的li标签
            li_arr = dom.xpath(xpath_items)
            for idx, li_each in enumerate(li_arr):
                # 截取
                _str = li_each.xpath('./a//text()')[0]
                str_arr = _str.split("\'")
                # print(22, str_arr)
                if len(str_arr) == 0:
                    continue

                # 解码
                _encode = str_arr[1]
                _title = base64.b64decode(_encode).decode()
                # print(_title)
                # exit()

                # 时间判断
                date_item = li_each.xpath(xpath_tip)[0]
                date_str = re.findall(r'[\[](.*?)[\]]', date_item)
                t = {'title': '[' + date_str[0] + '] ' + _title}
                # print(date_item, date_str[0])
                # exit()
                if date_str[0] < start_date:
                    print('Page: ' + str(page) + ', No: ' + str(idx + 1) + ', Title: ' + t[
                        "title"] + ', Href: ' + page_url, ', 开始时间小于：' + start_date, '\n')
                    flag = True
                    return data, flag

                # 判断是否包含keywords
                if bool(re.search("|".join(keywords), _title, re.I)):
                    _href = li_each.xpath(xpath_href)[0]

                    full_href = base_url + _href
                    t['href'] = xlwt.Formula('HYPERLINK("{}"; "{}")'.format(full_href, full_href))
                    t['url'] = full_href
                    print('Page: ' + str(page) + ', No: ' + str(idx + 1) + ', Title: ' + t[
                        "title"] + ', Href: ' + full_href,
                          '\n')
                    # print(t)
                    data.append(t)
                    time.sleep(random.randint(1, 3))

                    # 获取子页内容
                    # item_html = requests.get(full_href)
                    # item_html.encoding = item_html.apparent_encoding
                    # down_dom = etree.HTML(item_html.text)
                    # torrent_arr = down_dom.xpath(xpath_downbtn)
                    # if torrent_arr[0]:
                    #     down_page_url = base_url + torrent_arr[0]
                    #     print(torrent_arr)
                    #     exit()
                    #     if torrent_arr:
                    #         torrent = torrent_arr[0]
                    #         t['down'] = xlwt.Formula('HYPERLINK("{}"; "{}")'.format(base_url + torrent, base_url + torrent))
                    #         data.append(t)
                    #         time.sleep(random.randint(1, 3))

            return data, flag


# 获取每列所占用的最大列宽
def get_max_col(max_list):
    line_list = []
    # i表示行，j代表列
    for j in range(len(max_list[0])):
        line_num = []
        for i in range(len(max_list)):
            line_num.append(max_list[i][j])  # 将每列的宽度存入line_num
        line_list.append(max(line_num))  # 将每列最大宽度存入line_list
    return line_list


# 写入xls
def write_xls(data, file='test'):
    # 创建一个Workbook对象
    workbook = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 创建一个sheet对象
    worksheet = workbook.add_sheet('Sheet1', cell_overwrite_ok=True)

    worksheet.write(0, 0, "标题")
    worksheet.write(0, 1, "跳转")
    worksheet.write(0, 2, "url")

    # 列数
    # col_num = [0 for x in range(0, len(data) + 1)]
    # 记录每行每列宽度
    # col_list = []

    for i in range(len(data)):
        worksheet.write(i + 1, 0, data[i]["title"])
        worksheet.write(i + 1, 1, data[i]["href"])
        worksheet.write(i + 1, 2, data[i]["url"])

        # col_num[0] = len(data[i]["id"].encode('gb18030'))  # 计算每列值的大小
        # col_num[1] = len(data[i]["title"].encode('gb18030'))  # 计算每列值的大小
        # col_list.append(copy.copy(col_num))  # 记录一行每列写入的长度

        # 设置行高
        worksheet.row(i + 1).height_mismatch = True
        worksheet.row(i + 1).height = 20 * 24  # 20为基准数，20磅

    # 获取每列最大宽度
    # col_max_num = get_max_col(col_list)
    col_max_num = [80, 60, 40, 0]

    # 设置自适应列宽
    for i in range(0, len(col_max_num)):
        # 256*字符数得到excel列宽,为了不显得特别紧凑添加两个字符宽度
        worksheet.col(i).width = 256 * (col_max_num[i] + 2)

    # 保存excel文件
    workbook.save('D:/Code/python/data/' + file + '.xls')


# 读取 excel
def read_xls(file_name):
    path = f'../data/{file_name}.xls'
    df = pd.read_excel(path, sheet_name="Sheet1")
    data = df['url'].tolist()
    # print(len(data), data)
    # exit()
    # for idx, row in enumerate(data):
    #     print(idx, row, "\n")

    return data


# 批量自动打开
def open_browser(file_name):
    data = read_xls(file_name)
    num = 10
    m = 0
    for i, val in enumerate(data):
        chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
        crl = wb.get(chrome_path)
        if m > num:
            m = 0
            chrome_path_nw = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s --new-window"
            crl = wb.get(chrome_path_nw)
        crl.open(val)
        m += 1


def main():
    file_name = "keywords3_0528"
    open_browser(file_name)
    exit()
    start_time = time.perf_counter()
    data = []

    start_date = '05-20'

    keywords1 = ("91汝工作室", '乌克兰', '推特网红', '推特女神', '推特极品', '极品网红', '宅男福利',
                 '私人玩物', '超粉嫩美鲍', '骚+浪+贱', '骚 浪 贱', '91SWEATTT', 'HEGRE', '超正点',
                 )

    keywords2 = ("不见星空", '白袜袜格罗', '工口糯米姬', '押尾猫', '完具酱', '有喵酱',
                 '91蜜桃', '苏苏', "初音",
                 '希希酱', '绯红小猫', '橘子酱', '恶犬', '香草少女', '九尾狐狸', '沐沐睡不着呀', '可爱的小猫',
                 '来自喵星的岁酱', '露西宝宝', '原歆公主', '涂鸦少女', '小秋秋', '玩酱呀', '三寸', '软耳奶猫',
                 '娜美妖姬', '比卡丘', '亲亲我吖', '我刚成年', '软糖呀', '桃桃酱', '咬一口小奈樱',
                 '橘猫', '奈音', '小清殿下', "喵喵儿", '樱井奈奈', '怪污可优', '械师',
                 '夜夜主教', '赛高酱', '貂蝉', '王星雅', '浪味仙儿', '夏玲蔓', '涵北', '琉璃',
                 '发条', '习呆呆', '闵儿', 'KANAMI', '姚安琪', 'LEXISCANDYSHOP')
    keywords = ('教室', '91汝工作室', '乌克兰', '超粉嫩美鲍', '超正点')

    for i in range(1, 201):
        ret = get_page_data(i, data, keywords, start_date)
        data = ret[0]
        print('page' + str(i) + ' done!')
        if ret[1]:
            break
        time.sleep(random.randint(3, 6))

    if len(data):
        print('done! 共 {} 条'.format(len(data)))
        write_xls(data, file_name)
    else:
        print('data is empty!')

    delta = time.perf_counter() - start_time
    print("运行时间：{}秒".format(delta))


if __name__ == '__main__':
    main()
