# -*- coding: utf-8 -*-
"""
获取51job
"""
import requests
from lxml import etree
import csv
import codecs
import os

# 绝对路径
work_dir = os.path.dirname(os.path.abspath(__file__))
# 把当前路径切换到文件所在的路径
os.chdir(work_dir)

job_map = {
    'gokaifa': 'Go开发工程师',
    'phpkaifa': 'PHP开发工程师',
    'pachongkaifa': '爬虫工程师',
    'pythonkaifa': 'Python开发工程师',
}

# 网页链接
job_key = 'pachongkaifa'
url = f"https://jobs.51job.com/{job_key}/p"
# 请求头
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "guid=7e8a970a750a4e74ce237e74ba72856b; partner=blog_csdn_net",
    "Host": "jobs.51job.com",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
}

f = codecs.open(f'../../data/csv/{job_map[job_key]}岗位薪资.csv', 'a', 'utf-8')
writer = csv.writer(f)
writer.writerow(["岗位", "公司", "城市", "薪资"])

# 有请求头写法
for i in range(1, 14):
    res = requests.get(url=url + str(i), headers=headers)
    res.encoding = 'gbk'
    s = res.text
    selector = etree.HTML(s)
    for item in selector.xpath('/html/body/div[4]/div[2]/div[1]/div/div'):
        title = item.xpath('.//p/span[@class="title"]/a/text()')
        name = item.xpath('.//p/a/@title')
        location_name = item.xpath('.//p/span[@class="location name"]/text()')
        salary = item.xpath('.//p/span[@class="location"]/text()')
        time = item.xpath('.//p/span[@class="time"]/text()')
        if len(title) > 0 and len(name) > 0 and len(location_name) > 0 and len(salary) > 0:
            print(title)
            print(name)
            print(location_name)
            print(salary)
            try:
                writer.writerow([title[0] + "", name[0] + "", location_name[0] + "", salary[0] + ""])
            except:
                pass
            print("-----------")

f.close()
