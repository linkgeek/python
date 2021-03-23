import requests
import json
import xlwt
from lxml import etree
from bs4 import BeautifulSoup

def get_page_data(page, news):
    headers = {

    }

    params = {

    }

    url = "http://ac38.xyz/list.php?class=guochan&page=1"
    #response = requests.get("http://ac38.xyz/list.php?class=guochan&page=1", params=params, headers=headers)
    #html = etree.HTML(requests.get(url, headers=headers).text)

    soup = BeautifulSoup(url, "html.parser")
    title_url_Date = soup.find('ul', class_='list').find_all('li')
    for i in title_url_Date:
        # print(i)
        href = i.find('a')['href']
        print(href)


def write_data(news):
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
    for i in range(1, 2):
        news = get_page_data(i, news)
    print(news)

    #write_data(news)


if __name__ == '__main__':
    main()
