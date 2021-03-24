# encoding: utf-8

import requests
import json
import xlwt


def getData(page, news):
    headers = {
        "Host": "interface.sina.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": r"http://www.sina.com.cn/mid/search.shtml?range=all&c=news&q=%E6%97%85%E6%B8%B8&from=home&ie=utf-8",
        "Cookie": "ustat=__172.16.93.31_1580710312_0.68442000; genTime=1580710312; vt=99; Apache=9855012519393.69.1585552043971; SINAGLOBAL=9855012519393.69.1585552043971; ULV=1585552043972:1:1:1:9855012519393.69.1585552043971:; historyRecord={'href':'https://news.sina.cn/','refer':'https://sina.cn/'}; SMART=0; dfz_loc=gd-default",
        "TE": "Trailers"
    }

    params = {
        "t": "",
        "q": "旅游",
        "pf": "0",
        "ps": "0",
        "page": page,
        "stime": "2019-03-30",
        "etime": "2020-03-31",
        "sort": "rel",
        "highlight": "1",
        "num": "10",
        "ie": "utf-8"
    }

    response = requests.get("https://interface.sina.cn/homepage/search.d.json?", params=params, headers=headers)
    dic = json.loads(response.text)
    print(dic)
    exit(400)
    news += dic["result"]["list"]

    return news


def writeData(news):
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('新闻')

    worksheet.write(0, 0, "标题")
    worksheet.write(0, 1, "时间")
    worksheet.write(0, 2, "媒体")
    worksheet.write(0, 3, "网址")

    for i in range(len(news)):
        #print(news[i])
        worksheet.write(i + 1, 0, news[i]["origin_title"])
        worksheet.write(i + 1, 1, news[i]["datetime"])
        worksheet.write(i + 1, 2, news[i]["media"])
        worksheet.write(i + 1, 3, news[i]["url"])

    workbook.save('../data/sina-news.xls')


def main():
    news = []
    for i in range(1, 10):
        news = getData(i, news)
    writeData(news)


if __name__ == '__main__':
    main()
