import requests
from lxml import etree
import xlwt

url = 'https://www.baidu.com/'

headers = {
    'Host': 'www.baidu.com',
    'Referer': 'https://www.baidu.com/',
    'Cookie': 'BIDUPSID=BD8E48DC84DCABED7D99345FF5E43BA2; PSTM=1614323196; BAIDUID=BD8E48DC84DCABEDFBEB5E923999C22F:FG=1; BD_UPN=12314753; __yjs_duid=1_45dc49a38181f6065a836f0fa159d6b31614327352736; BDUSS_BFESS=Tl4YmdwMUNEMk1wOFJLYjV3REoxRElhT2ZJMzlsU0xRR1h5Z3JnRjhkdjdDVzFnSUFBQUFBJCQAAAAAAAAAAAEAAADriHI3aGV6aGFuYW5nZWwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPt8RWD7fEVgS; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BAIDUID_BFESS=BD8E48DC84DCABEDFBEB5E923999C22F:FG=1; delPer=0; BD_CK_SAM=1; Hm_lvt_aec699bb6442ba076c8981c6dc490771=1615976118,1616377244,1616468482,1616482875; BD_HOME=1; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; __yjsv5_shitong=1.0_7_6a77bb2424a572271691fd6125718684e64f_700_1616547994534_218.17.158.162_e6464a48; shifen[233830276218_5342]=1616555976; BCLID=11504149738746468476; BDSFRCVID=db_OJeC624QiGjTeSiHLrge6nHG3phbTH6q21otlQSGkewrt-QivEG0POU8g0KAbGxQJogKK3gOTH4PF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF=tbCfVCPXJCvbfP0kh-Q_KtjH-UnLqhLD3gOZ0l8KtfF5ODJV-4or0nLyKxJ-tt6-Lj-qQxjmWIQHDp3MbJbzhbkeQljHLfKjJG54KKJxfPPWeIJo5DcaQjQQhUJiB5JMBan7_UJIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtnLhbC8ljTuWejQM5pJfet7Kaj6asJOOaCvjVpROy4oTj6DlDPujB4j-Xa7H0toj5CQ_efo9jRQG3MvB-fnxQPQeWCJOWhQK-fQPhK5XQft205kbeMtjBbLL-mIton7jWhk5ep72y5OmQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8EjHCHt6ttJnID_IvJabbEDR0kMtcohPJH-UnLqhcg3gOZ0l8KtDTTJM7ej4ooWj_ZKxJ-tt6BJGRh3DOmWIQHDU51-PrW0pkshG0ey-jTWR64KKJxfPPWeIJo5t50-U0XhUJiB5JMBan7_UJIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtnLhbC8lj5_Ke5ObepJf-K6B-TTeBTrJaDvAsx7Oy4oTj6j3jPTrt4R-L2O0Ltoj5CQ_eqk4blnD3MvB-fnNb6bRKCbt3RTjQn7x8M3PQft205kbeMtjBbQab6u8Qn7jWhk5ep72y5OmQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8EjHCeJ6KfJJ4DoIv5b-0_HRT1Mt5Eh-cH-UnLq-3aX2OZ0l8KtDbGjq3F3-o6MfkTKxJ-tt673b7jBnomWIQahCjv5-vG0U-fbqJH-IrI26c4KKJxBMKWeIJoLt5n2h_phUJiB5JMBan7_UJIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtnLhbRO4-TFKjTvQjMK; BCLID_BFESS=11504149738746468476; BDSFRCVID_BFESS=db_OJeC624QiGjTeSiHLrge6nHG3phbTH6q21otlQSGkewrt-QivEG0POU8g0KAbGxQJogKK3gOTH4PF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF_BFESS=tbCfVCPXJCvbfP0kh-Q_KtjH-UnLqhLD3gOZ0l8KtfF5ODJV-4or0nLyKxJ-tt6-Lj-qQxjmWIQHDp3MbJbzhbkeQljHLfKjJG54KKJxfPPWeIJo5DcaQjQQhUJiB5JMBan7_UJIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtnLhbC8ljTuWejQM5pJfet7Kaj6asJOOaCvjVpROy4oTj6DlDPujB4j-Xa7H0toj5CQ_efo9jRQG3MvB-fnxQPQeWCJOWhQK-fQPhK5XQft205kbeMtjBbLL-mIton7jWhk5ep72y5OmQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8EjHCHt6ttJnID_IvJabbEDR0kMtcohPJH-UnLqhcg3gOZ0l8KtDTTJM7ej4ooWj_ZKxJ-tt6BJGRh3DOmWIQHDU51-PrW0pkshG0ey-jTWR64KKJxfPPWeIJo5t50-U0XhUJiB5JMBan7_UJIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtnLhbC8lj5_Ke5ObepJf-K6B-TTeBTrJaDvAsx7Oy4oTj6j3jPTrt4R-L2O0Ltoj5CQ_eqk4blnD3MvB-fnNb6bRKCbt3RTjQn7x8M3PQft205kbeMtjBbQab6u8Qn7jWhk5ep72y5OmQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8EjHCeJ6KfJJ4DoIv5b-0_HRT1Mt5Eh-cH-UnLq-3aX2OZ0l8KtDbGjq3F3-o6MfkTKxJ-tt673b7jBnomWIQahCjv5-vG0U-fbqJH-IrI26c4KKJxBMKWeIJoLt5n2h_phUJiB5JMBan7_UJIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtnLhbRO4-TFKjTvQjMK; H_PS_PSSID=33241_33742_33272_31254_33691_33758_33392_26350_33266; BDRCVFR[S4-dAuiWMmn]=I67x6TjHwwYf0; ab_sr=1.0.0_ZjlmZmNkODRlMTc3YzdjMWZmODkxZTMyMzQxODJlMjE3MTQyYTU5MGFiZmM1Y2M1OTI1NDU0NDQ0YTYxOGI5MGM0NWI4MGVlMzE5MjE1MWQxMTliYjZhMjRlMzhiMmQw; Hm_lpvt_aec699bb6442ba076c8981c6dc490771=1616579945; sugstore=1; PSINO=3; H_PS_645EC=4e4aLReUlrYiLA1PbstR7greqY7gKs%2BAtZL1pimz%2BCasr365HRiQoaTYnNGqQB547LCo; BA_HECTOR=0121048ka52g202kbq1g5m3u50r; BDSVRTM=0; COOKIE_SESSION=672_0_9_5_31_0_0_0_9_0_0_0_78_0_58_0_1616580606_0_1616580548%7C9%23178483_29_1616555713%7C6',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
}

# 获取所有 li标签
xpath_items = '//ul[@class="s-news-rank-content"]/li'
xpath_son_items = '//ul[@class="s-news-rank-content"]/li'

# 对每个 li标签再提取
xpath_href = './a/@href'
xpath_rank = './a/span[1]/text()'
xpath_title = './a/span[2]/text()'
xpath_view = './div/text()'

# 分页获取
def get_page_data(page, data):
    r = requests.get(url, headers=headers)
    r.encoding = r.apparent_encoding
    dom = etree.HTML(r.text)

    # 获取所有的文章标签
    liArr = dom.xpath(xpath_items)
    #print(liArr)
    #exit(11)

    # 分别对每一个文章标签进行操作 将每篇文章的链接 标题 评论数 点赞数放到一个字典里
    for item in liArr:
        t = {}
        _title = item.xpath(xpath_title)[0]
        #print(item)
        #exit(22)

        t['href'] = item.xpath(xpath_href)[0]
        t['rank'] = item.xpath(xpath_rank)[0]
        t['title'] = _title
        t['view'] = item.xpath(xpath_view)[0]
        data.append(t)

        # searchStr = "台湾"
        # if _title.find(searchStr) >= 0:
        #     _href = item.xpath(xpath_href)[0]
        #     # 获取子页内容
        #     html = requests.get(_href, headers=headers)
        #     html.encoding = html.apparent_encoding
        #     dom2 = etree.HTML(html.text)
        #     itemArr = dom.xpath(xpath_son_items)


# 写入xls
def write_xls(data):
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('热搜榜')

    worksheet.write(0, 0, "序号")
    worksheet.write(0, 1, "关键字")
    worksheet.write(0, 2, "阅读量")
    worksheet.write(0, 3, "链接")
    worksheet.write(0, 4, "导语")

    for i in range(len(data)):
        # print(news[i])
        worksheet.write(i + 1, 0, data[i]["rank"])
        worksheet.write(i + 1, 1, data[i]["keyword"])
        worksheet.write(i + 1, 2, data[i]["view"])
        worksheet.write(i + 1, 3, data[i]["href"])
        worksheet.write(i + 1, 4, data[i]["topic"])

    workbook.save('../data/test22.xls')


def main():
    data = []
    data = get_page_data(1, data)
    # for i in range(1, 2):
    # news = get_page_data(i, news)
    print(data)
    exit(11)
    write_xls(data)


if __name__ == '__main__':
    main()