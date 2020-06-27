###导入模块
import requests
from lxml import etree

###网址
url = "https://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6"
###模拟浏览器
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}


###主函数
def main():
    ###获取html页面
    html = etree.HTML(requests.get(url, headers=header).text)
    rank = html.xpath('//td[@class="td-01 ranktop"]/text()')
    affair = html.xpath('//td[@class="td-02"]/a/text()')
    href = html.xpath('//td[@class="td-02"]/a/@href')
    view = html.xpath('//td[@class="td-02"]/span/text()')
    # print(affair, href)
    # exit(11)

    top = affair[0]
    affair = affair[1:]
    print('{0:<10}\t{1:<40}'.format("top", top))

    """
    格式说明符前面有一个冒号：，{字段名!转换字段:格式说明符}。其中格式说明符本身可以是一个字段名
    对齐方式：(<)左对齐；(>)右对齐；(^)居中；(=)在正负号（如果有的话）和数字之间填充，该对齐选项仅对数字类型有效。
    """
    # tplt = "{0:<10}\t{1:{3}<30}\t{2:{3}>20}"
    tplt = "{0:<10}\t{1:{4}<16}\t{2:<10}\t{3:<10}"
    # tplt = "{0:^6}\t{1:{4}^10}\t{2:^10}\t{3:^10}"
    for i in range(0, len(affair)):
        # print("{0:<10}\t{1:{3}<30}\t{2:{3}>20}\t{3:^10}".format(rank[i], affair[i], view[i], href[i], chr(12288)))
        print(tplt .format(rank[i], affair[i], view[i], href[i], chr(12288)))


main()
