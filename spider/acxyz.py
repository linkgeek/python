#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import etree
import xlwt
import time
import base64
import random
import re

base_url = 'http://www.btmj.xyz/'
url = base_url + 'list.php?class=guochan'

headers = {
    'Host': 'www.btdk.xyz',
    'Cookie': '__cfduid=d300ba300215e7290574d0bd7cdf617551620403510; _ga=GA1.1.1094315111.1620403509; _ga_Q3P79YL0DW=GS1.1.1620403509.1.1.1620405639.0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',

    # 'Host': 'ap.lijit.com',
    # 'Cookie': 'ljt_reader=c3baa883549c172a9fcf1b58;Version=1;Domain=.lijit.com;Path=/;Max-Age=31536000;Secure; SameSite=None;',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46',
}

# 获取所有 li标签
xpath_items = '//div[@id="content"]/div/ul/li[position()>1][position()<last()]'
xpath_downbtn = '//div[@class="download"]/b//a/@href'
xpath_down = '//div[@class="download"]/b//a/@href'

# 对每个 li标签再提取
xpath_tip = './text()'
xpath_href = './a/@href'
xpath_title = './/text()'


# 分页获取
def get_page_data(page, data, keywords, start_date):
    page_url = url + '&page=' + str(page)
    while True:
        try:
            r = requests.get(page_url, headers=headers, timeout=15)
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
                # 时间
                date_item = li_each.xpath(xpath_tip)[0]
                date_str = re.findall(r'[\[](.*?)[\]]', date_item)
                if date_str[0] < start_date:
                    print('Page: ' + str(page) + ', No: ' + str(idx + 1) + ', 开始时间小于：' + start_date, '\n')
                    return data

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

                # 判断是否包含keywords
                if bool(re.search("|".join(keywords), _title, re.I)):
                    _href = li_each.xpath(xpath_href)[0]
                    t = {'title': date_item[0] + _title}
                    full_href = base_url + _href
                    t['href'] = xlwt.Formula('HYPERLINK("{}"; "{}")'.format(full_href, full_href))
                    # t['down'] = full_href
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

            return data


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
    worksheet = workbook.add_sheet('资源', cell_overwrite_ok=True)

    worksheet.write(0, 0, "标题")
    worksheet.write(0, 1, "链接")
    # worksheet.write(0, 2, "下载")

    # 列数
    # col_num = [0 for x in range(0, len(data) + 1)]
    # 记录每行每列宽度
    # col_list = []

    for i in range(len(data)):
        worksheet.write(i + 1, 0, data[i]["title"])
        worksheet.write(i + 1, 1, data[i]["href"])
        # worksheet.write(i + 1, 2, data[i]["down"])

        # col_num[0] = len(data[i]["id"].encode('gb18030'))  # 计算每列值的大小
        # col_num[1] = len(data[i]["title"].encode('gb18030'))  # 计算每列值的大小
        # col_list.append(copy.copy(col_num))  # 记录一行每列写入的长度

        # 设置行高
        worksheet.row(i + 1).height_mismatch = True
        worksheet.row(i + 1).height = 20 * 24  # 20为基准数，20磅

    # 获取每列最大宽度
    # col_max_num = get_max_col(col_list)
    col_max_num = [80, 60, 0]

    # 设置自适应列宽
    for i in range(0, len(col_max_num)):
        # 256*字符数得到excel列宽,为了不显得特别紧凑添加两个字符宽度
        worksheet.col(i).width = 256 * (col_max_num[i] + 2)

    # 保存excel文件
    workbook.save('D:/Code/python/data/' + file + '.xls')


def main():
    start_time = time.perf_counter()
    data = []
    keywords1 = ("91汝工作室", '乌克兰', '推特网红', '推特女神', '推特极品', '极品网红', '宅男福利',
                 '私人玩物', '女仆', '超粉嫩美鲍', '骚+浪+贱', '骚 浪 贱', '91SWEATTT', 'HEGRE', '超正点')
    keywords = ('希希酱', '绯红小猫', '橘子酱', '恶犬', '香草少女', '九尾狐狸', '沐沐睡不着呀',
                '来自喵星的岁酱', '露西宝宝', '原歆公主', '涂鸦少女', '小秋秋', '玩酱呀', '三寸',
                '娜美妖姬', '比卡丘', '亲亲我吖', '我刚成年', '软糖呀', '桃桃酱',
                '橘猫', '奈音', '小清殿下', "喵喵儿", '樱井奈奈', '怪污可优', '悠宝', '械师',
                '夜夜主教', '赛高酱', '貂蝉', '王星雅', '浪味仙儿',
                '发条', '习呆呆', '闵儿', '可爱的小猫', 'KANAMI', '姚安琪', 'LEXISCANDYSHOP',)

    keywords3 = ("不见星空", '白袜袜格罗', '工口糯米姬', '押尾猫', "初音", '完具酱', '有喵酱',
                 '91蜜桃', '小鸟酱', '苏苏')

    file_name = "keywords2_0523_0523"
    start_date = '05-23'
    for i in range(1, 11):
        data = get_page_data(i, data, keywords, start_date)
        print('page' + str(i) + ' done!')
        time.sleep(random.randint(2, 4))

    if len(data):
        print('done! 共 {} 条'.format(len(data)))
        write_xls(data, file_name)
    else:
        print('data is empty!')

    delta = time.perf_counter() - start_time
    print("运行时间：{}秒".format(delta))


if __name__ == '__main__':
    main()
