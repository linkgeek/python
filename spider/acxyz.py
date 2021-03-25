import requests
from lxml import etree
import xlwt
import time
import re

base_url = 'http://ac38.xyz/'
url = 'http://ac38.xyz/list.php?class=guochan&page='

headers = {
    'Host': 'ac38.xyz',
    # 'Referer': 'https://www.baidu.com/',
    'Cookie': '__cfduid=de73110f83595c0f98b2d5f7bbadc485a1616254803; _ga=GA1.1.2006431600.1616254805; _ga_Q3P79YL0DW=GS1.1.1616593392.5.1.1616600045.0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
}

# 获取所有 li标签
xpath_items = '//ul[@class="list"]/li[position()>1]'
xpath_down = '//div[@class="download"]/p[1]/a/@href'

# 对每个 li标签再提取
xpath_href = './a/@href'
xpath_title = './a//text()'
xpath_title_basic = './a/text()'


# 分页获取
def get_page_data(page, data, search_str):
    page_url = url + str(page)

    r = requests.get(page_url, headers=headers)
    r.encoding = r.apparent_encoding
    dom = etree.HTML(r.text)


    # 获取所有的文章标签
    li_arr = dom.xpath(xpath_items)
    #print(li_arr)
    #exit(22)

    # 分别对每一个文章标签进行操作 将每篇文章的链接 标题 评论数 点赞数放到一个字典里
    for idx, li_each in enumerate(li_arr):

        # _title = li_each.xpath(xpath_title)
        #for bad in li_each.xpath('./a/script'):
            #bad.getparent().remove(bad)

        content = li_each.xpath("string(.)")
        content2 = li_each.xpath('./a')
        #content = ' '.join([i.strip() for i in content])[1:]
        print(content)
        print(2, content2)
        exit(22)

        tip_title = ''.join(li_each.xpath(xpath_title)).strip()
        _title = ''.join(li_each.xpath(xpath_title_basic)).lstrip().rstrip()
        print(idx + 1, tip_title, _title)
        exit(1)

        search_str = "ymdd"
        if _title.find(search_str) >= 0:
            t = {}
            _href = li_each.xpath(xpath_href)[0]
            # 获取子页内容
            son_href = base_url + _href
            item_html = requests.get(son_href, headers=headers)
            item_html.encoding = item_html.apparent_encoding
            dom2 = etree.HTML(item_html.text)

            print(idx + 1, dom2.xpath(xpath_down))
            # exit(555)
            t['id'] = idx + 1
            t['title'] = tip_title + _title
            t['href'] = base_url + _href

            torrent_arr = dom2.xpath(xpath_down)
            torrent = ''
            if torrent_arr:
                torrent = torrent_arr[0]
            # t['torrent'] = base_url + torrent
            # xlwt.Formula('"test " & HYPERLINK("http://google.com")')
            t['torrent'] = xlwt.Formula('HYPERLINK("{}"; "{}")'.format(base_url + torrent, base_url + torrent))
            # print(t)
            # exit(33)
            data.append(t)

        time.sleep(3)

    return data


# 写入xls
def write_xls(data):
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('资源')

    worksheet.write(0, 0, "序号")
    worksheet.write(0, 1, "标题")
    worksheet.write(0, 2, "链接")
    worksheet.write(0, 3, "下载")

    for i in range(len(data)):
        # print(news[i])
        worksheet.write(i + 1, 0, data[i]["id"])
        worksheet.write(i + 1, 1, data[i]["title"])
        worksheet.write(i + 1, 2, data[i]["href"])
        worksheet.write(i + 1, 3, data[i]["torrent"])

    workbook.save('../data/acxyz.xls')


def main():
    data = []
    search_str = "台湾"
    data = get_page_data(1, data, search_str)
    # for i in range(1, 2):
    # data = get_page_data(i, data, search_str)
    # print(data)
    # exit(66)
    write_xls(data)


if __name__ == '__main__':
    main()
