# 导入模块
import requests
from lxml import etree
import xlwt

# 网址
url = "https://www.baidu.com/"
# 模拟浏览器
header0 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
}
header = {
    'Host': 'www.baidu.com',
    'Referer': 'https://www.baidu.com/',
    'Cookie': 'BIDUPSID=D99314F8A5E53EA50B85C37A0D96C400; PSTM=1576140470; HOSUPPORT=1; BAIDUID=490062CDE50C5B626A1882E6938F5EE7:FG=1; UBI=fi_PncwhpxZ%7ETaJc9oaTqIbsWBE38p5LUoO; H_WISE_SIDS=149390_148169_142018_148320_147088_147893_148867_148208_148875_148435_147279_148001_148823_147828_148439_148754_147890_146573_148524_147346_127969_147239_147351_147024_131953_146732_138426_145988_131423_144659_142209_147527_107311_149269_140312_146396_144966_149279_145607_148662_148345_148049_148749_147546_146053_148869_110085; MCITY=-131%3A; HOSUPPORT_BFESS=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; pplogid_BFESS=4262olGrh4bA0KVJ%2BhEixRGiLx8E%2B%2B%2FlsYrZ1z21%2BuY58eW%2FOkM3jLZkH843E9obSHAaoWXHmisIG1fW93Ig0dG9g2y7NVpEpnh6NRQpF8wmiJo%3D;pplogid=5537awLy1oSevWNkHr4Lz7C1fsWUtVYZZdx0rJKkaAmCX1eMtEjfaor2R1DB0I%2Bj89BQviWor0ElEE8HF%2Bd8mbRKA5fTGfpkTrv3KJZYlkGnHcQ%3D; BDSFRCVID=An_OJexroG3_iS6rKjsQEX1OKgKK0gOTDYLEOwXPsp3LGJLVN4vPEG0Pt_U-mEt-J8jwogKK0gOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tbkD_C-MfIvDqTrP-trf5DCShUFs-MuOB2Q-XPoO3KOrjf8CKxR8XPCkWaQ9B-biWbRM2MbgylRp8P3y0bb2DUA1y4vpWj3qLgTxoUJ2XMKVDq5mqfCWMR-ebPRiJPb9Qg-qahQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hI0ljj82e5PVKgTa54cbb4o2WbCQtR6P8pcN2b5oQTtmMJ-qbfnBB2o4hIjvWb3vOIJTXpOUWfAkXpJvQnJjt2JxaqRCBDb-Vh5jDh3MBpQDhtoJexIO2jvy0hvctn3cShPCyUjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhDNtDt60jfn3aQ5rtKRTffjrnhPF3Xl43XP6-hnjy3b7dBx8K-qv88PQHW5QcyP-UyN3MWh3RymJ42-39LPO2hpRjyxv4X60B0-oxJpOJXaILWl52HlFWj43vbURvD--g3-AqBM5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIEoK0hJC-2bKvPKITD-tFO5eT22-usJerT2hcHMPoosIO3Mq--KxPqKU74XTo9WKviaKJjBMbUoqRHXnJi0btQDPvxBf7pBJnqbp5TtUJM_UKzhfoMqfTbMlJyKMnitIv9-pPKWhQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKuDTtajj3QeaRabK6aKC5bL6rJabC3EJr3XU6q2bDeQNbdaltq-e3BQMjNyIjcOn3oyT3JXp0vWtv4WbbvLT7johRTWqR48CbC0MonDh83Bn_L2xQJHmLOBt3O5hvvhb3O3MA-yUKmDloOW-TB5bbPLUQF5l8-sq0x0bOte-bQXH_E5bj2qRFtoC8-3q; delPer=0; PSINO=1; BDRCVFR[X_XKQks0S63]=mk3SLVN4HKm; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; BDRCVFR[S4-dAuiWMmn]=I67x6TjHwwYf0; H_PS_PSSID=32288_1467_32359_32328_32046_32399_32429_32116_32089_26350_31639',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
}

# 分页获取
def get_page_data(page, news):
    # 获取html页面
    html = etree.HTML(requests.get(url, headers=header).text)

    # print(11, html)

    # // 相对路径查找
    #  / 或 // 即可查找元素的子节点或子孙节点
    # 查询父节点可以用 … 来实现
    rank = html.xpath('//li/a/span[@class="title-content-index"]/text()')
    title = html.xpath('//li/a/span[@class="title-content-title"]/text()')
    href = html.xpath('//li/a/@href')
    view = html.xpath('//li/div/text()')
    print(rank, title, href, view)
    exit(11)

    affair = []

    """
    格式说明符前面有一个冒号：，{字段名!转换字段:格式说明符}。其中格式说明符本身可以是一个字段名
    对齐方式：(<)左对齐；(>)右对齐；(^)居中；(=)在正负号（如果有的话）和数字之间填充，该对齐选项仅对数字类型有效。
    """

    tplt = "{0:<10}\t{1:{4}<16}\t{2:<10}\t{3:<10}"
    for i in range(0, len(affair)):
        # print(tplt.format(rank[i], affair[i], view[i], href[i], chr(12288)))

        topic = ''
        _href = href[i]
        if href[i]:
            _href = 'https://s.weibo.com/' + href[i]
            _html = etree.HTML(requests.get(_href, headers=header).text)
            _topic = _html.xpath('//div[@class="card card-topic-lead s-pg16"]/p/text()')
            #print(_topic)
            #exit(14)
            if _topic:
                topic = _topic[0]

        obj = {"rank": rank[i], "keyword": affair[i], "view": view[i], "href": _href, "topic": topic}
        news.append(obj)
    return news


# 写入xls
def write_xls(news):
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('热搜榜')

    worksheet.write(0, 0, "序号")
    worksheet.write(0, 1, "关键字")
    worksheet.write(0, 2, "阅读量")
    worksheet.write(0, 3, "链接")
    worksheet.write(0, 4, "导语")

    for i in range(len(news)):
        # print(news[i])
        worksheet.write(i + 1, 0, news[i]["rank"])
        worksheet.write(i + 1, 1, news[i]["keyword"])
        worksheet.write(i + 1, 2, news[i]["view"])
        worksheet.write(i + 1, 3, news[i]["href"])
        worksheet.write(i + 1, 4, news[i]["topic"])

    workbook.save('../data/realtimehot.xls')


def main():
    news = []
    news = get_page_data(1, news)
    # for i in range(1, 2):
    # news = get_page_data(i, news)
    # print(news)
    # exit(11)
    write_xls(news)


if __name__ == '__main__':
    main()
