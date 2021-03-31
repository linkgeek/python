#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import etree
import xlwt
import time
import base64
import copy

base_url = 'http://ac38.xyz/'
# url = 'http://ac38.xyz/list.php?class=guochan'
url = 'http://ac38.xyz/list.php?class=riben'

headers = {
    'Host': 'ac38.xyz',
    # 'Referer': 'https://www.baidu.com/',
    'Cookie': '__cfduid=de73110f83595c0f98b2d5f7bbadc485a1616254803; _ga=GA1.1.2006431600.1616254805; _ga_Q3P79YL0DW=GS1.1.1616593392.5.1.1616600045.0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
}

# 获取所有 li标签
xpath_items = '//div[@id="content"]/div/ul/li[position()>1][position()<last()]'
xpath_down = '//div[@class="download"]/p[1]/a/@href'

# 对每个 li标签再提取
xpath_tip = './text()'
xpath_href = './a/@href'
xpath_title = './/text()'


# 分页获取
def get_page_data(page, data, search_str):
    page_url = url + '&page=' + str(page)
    r = requests.get(page_url)
    r.encoding = r.apparent_encoding
    dom = etree.HTML(r.text)

    # 获取所有的文章标签
    li_arr = dom.xpath(xpath_items)
    # print(page_url, li_arr)
    # exit()

    # 分别对每一个文章标签进行操作 将每篇文章的链接 标题 评论数 点赞数放到一个字典里
    for idx, li_each in enumerate(li_arr):
        t = {}
        # ele = li_each.xpath('.//script | //noscript')
        # for e in ele:
        #     e.getparent().remove(e)

        _str = li_each.xpath('./a//text()')[0]
        # print(_str)

        # 截取
        str_arr = _str.split("\'")
        # print(idx + 1, _str, str_arr)

        if len(str_arr) == 0:
            continue

        _encode = str_arr[1]
        # 解码
        _title = base64.b64decode(_encode).decode()
        # print(_title)
        # exit(22)

        _tip = li_each.xpath(xpath_tip)[0]
        _href = li_each.xpath(xpath_href)[0]
        t['id'] = str(idx + 1)
        t['title'] = _tip + _title
        # t['href'] = base_url + _href
        full_href = base_url + _href
        t['href'] = xlwt.Formula('HYPERLINK("{}"; "{}")'.format(full_href, full_href))

        if _title.find(search_str) >= 0:
            print('Page: ' + str(page) + ', No: ' + str(idx + 1) + ', Title: ' + t["title"] + ', Href: ' + full_href,
                  '\n')

            # 获取子页内容
            item_html = requests.get(full_href)
            item_html.encoding = item_html.apparent_encoding
            down_dom = etree.HTML(item_html.text)
            torrent_arr = down_dom.xpath(xpath_down)

            if torrent_arr:
                torrent = torrent_arr[0]
                t['down'] = xlwt.Formula('HYPERLINK("{}"; "{}")'.format(base_url + torrent, base_url + torrent))
                # print(t)
                # exit(33)
                data.append(t)
                time.sleep(3)

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
def write_xls(data, file='acxyz'):
    # 创建一个Workbook对象
    workbook = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 创建一个sheet对象
    worksheet = workbook.add_sheet('资源', cell_overwrite_ok=True)

    worksheet.write(0, 0, "序号")
    worksheet.write(0, 1, "标题")
    worksheet.write(0, 2, "链接")
    worksheet.write(0, 3, "下载")

    # 列数
    col_num = [0 for x in range(0, len(data) + 1)]
    # print(data, '\n', col_num, '\n')
    # exit()

    # 记录每行每列宽度
    col_list = []

    for i in range(len(data)):
        worksheet.write(i + 1, 0, data[i]["id"])
        worksheet.write(i + 1, 1, data[i]["title"])
        worksheet.write(i + 1, 2, data[i]["href"])
        worksheet.write(i + 1, 3, data[i]["down"])

        col_num[0] = len(data[i]["id"].encode('gb18030'))  # 计算每列值的大小
        col_num[1] = len(data[i]["title"].encode('gb18030'))  # 计算每列值的大小
        col_list.append(copy.copy(col_num))  # 记录一行每列写入的长度

    # 获取每列最大宽度
    # col_max_num = get_max_col(col_list)
    col_max_num = [2, 120, 60, 40, 0]
    # print(col_max_num, '\n')
    # exit()

    # 设置自适应列宽
    for i in range(0, len(col_max_num)):
        # 256*字符数得到excel列宽,为了不显得特别紧凑添加两个字符宽度
        worksheet.col(i).width = 256 * (col_max_num[i] + 2)

    # 保存excel文件
    workbook.save('D:/Code/python/data/' + file + '.xls')


def main():
    start_time = time.perf_counter()
    data = []
    search_str = "SY"
    file_name = "acsy"
    # data = get_page_data(1, data, search_str)
    for i in range(1, 65):
        data = get_page_data(i, data, search_str)
        print('page' + str(i) + ' done!')
        time.sleep(3)

    # print('\n', data)
    # exit(66)

    if len(data):
        print('done! 共 {} 条'.format(len(data)))
        write_xls(data, file_name)
    else:
        print('data is empty!')

    delta = time.perf_counter() - start_time
    print("运行时间：{}秒".format(delta))


if __name__ == '__main__':
    main()
