# 天天基金股吧、贴吧
import csv
import time
import random
import requests
import traceback
from time import sleep
from fake_useragent import UserAgent
from lxml import etree


def gen_fund_csv(fund_code):
    for page in range(1, 6372):  # 爬取多页（共6371页）
        html = get_fund(fund_code, page)
        parse_fund(html, fund_code)
        time.sleep(random.uniform(1, 2))
        print(f"第{page}页提取完成")


def get_fund(fund_code, page):
    em_headers = {
        "User-Agent": UserAgent(verify_ssl=False).random
    }
    es_url = f'http://guba.eastmoney.com/list,of{fund_code}_{page}.html'
    resp = requests.get(es_url, headers=em_headers, timeout=10)
    return resp


def parse_fund(resp, fund_code):
    parse = etree.HTML(resp.text)  # 解析网页
    items = parse.xpath('//*[@id="articlelistnew"]/div')[1:91]
    for item in items:
        item = {
            '阅读': ''.join(item.xpath('./span[1]/text()')).strip(),
            '评论': ''.join(item.xpath('./span[2]/text()')).strip(),
            '标题': ''.join(item.xpath('./span[3]/a/text()')).strip(),
            '作者': ''.join(item.xpath('./span[4]/a/font/text()')).strip(),
            '时间': ''.join(item.xpath('./span[5]/text()')).strip()
        }

        print(item)
        with open(f'./{fund_code}.csv', 'a', encoding='utf_8_sig', newline='') as fp:
            fieldnames = ['阅读', '评论', '标题', '作者', '时间']
            writer = csv.DictWriter(fp, fieldnames)
            writer.writerow(item)


# 获取贴吧数据
def main():
    fund_code = 161725
    gen_fund_csv(fund_code)


if __name__ == '__main__':
    main()
