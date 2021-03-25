import requests
import re
import urllib.parse
from lxml import etree

url = 'https://www.baidu.com/'

headers = {
    'Host': 'www.baidu.com',
    'Referer': 'https://www.baidu.com/',
    'Cookie': 'BIDUPSID=D99314F8A5E53EA50B85C37A0D96C400; PSTM=1576140470; HOSUPPORT=1; BAIDUID=490062CDE50C5B626A1882E6938F5EE7:FG=1; UBI=fi_PncwhpxZ%7ETaJc9oaTqIbsWBE38p5LUoO; H_WISE_SIDS=149390_148169_142018_148320_147088_147893_148867_148208_148875_148435_147279_148001_148823_147828_148439_148754_147890_146573_148524_147346_127969_147239_147351_147024_131953_146732_138426_145988_131423_144659_142209_147527_107311_149269_140312_146396_144966_149279_145607_148662_148345_148049_148749_147546_146053_148869_110085; MCITY=-131%3A; HOSUPPORT_BFESS=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; pplogid_BFESS=4262olGrh4bA0KVJ%2BhEixRGiLx8E%2B%2B%2FlsYrZ1z21%2BuY58eW%2FOkM3jLZkH843E9obSHAaoWXHmisIG1fW93Ig0dG9g2y7NVpEpnh6NRQpF8wmiJo%3D;pplogid=5537awLy1oSevWNkHr4Lz7C1fsWUtVYZZdx0rJKkaAmCX1eMtEjfaor2R1DB0I%2Bj89BQviWor0ElEE8HF%2Bd8mbRKA5fTGfpkTrv3KJZYlkGnHcQ%3D; BDSFRCVID=An_OJexroG3_iS6rKjsQEX1OKgKK0gOTDYLEOwXPsp3LGJLVN4vPEG0Pt_U-mEt-J8jwogKK0gOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tbkD_C-MfIvDqTrP-trf5DCShUFs-MuOB2Q-XPoO3KOrjf8CKxR8XPCkWaQ9B-biWbRM2MbgylRp8P3y0bb2DUA1y4vpWj3qLgTxoUJ2XMKVDq5mqfCWMR-ebPRiJPb9Qg-qahQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hI0ljj82e5PVKgTa54cbb4o2WbCQtR6P8pcN2b5oQTtmMJ-qbfnBB2o4hIjvWb3vOIJTXpOUWfAkXpJvQnJjt2JxaqRCBDb-Vh5jDh3MBpQDhtoJexIO2jvy0hvctn3cShPCyUjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhDNtDt60jfn3aQ5rtKRTffjrnhPF3Xl43XP6-hnjy3b7dBx8K-qv88PQHW5QcyP-UyN3MWh3RymJ42-39LPO2hpRjyxv4X60B0-oxJpOJXaILWl52HlFWj43vbURvD--g3-AqBM5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIEoK0hJC-2bKvPKITD-tFO5eT22-usJerT2hcHMPoosIO3Mq--KxPqKU74XTo9WKviaKJjBMbUoqRHXnJi0btQDPvxBf7pBJnqbp5TtUJM_UKzhfoMqfTbMlJyKMnitIv9-pPKWhQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKuDTtajj3QeaRabK6aKC5bL6rJabC3EJr3XU6q2bDeQNbdaltq-e3BQMjNyIjcOn3oyT3JXp0vWtv4WbbvLT7johRTWqR48CbC0MonDh83Bn_L2xQJHmLOBt3O5hvvhb3O3MA-yUKmDloOW-TB5bbPLUQF5l8-sq0x0bOte-bQXH_E5bj2qRFtoC8-3q; delPer=0; PSINO=1; BDRCVFR[X_XKQks0S63]=mk3SLVN4HKm; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; BDRCVFR[S4-dAuiWMmn]=I67x6TjHwwYf0; H_PS_PSSID=32288_1467_32359_32328_32046_32399_32429_32116_32089_26350_31639',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
}


def get_data():
    response = requests.get(url, headers=headers).content.decode('utf-8')

    # 获取关键字
    pat = '"pure_title": "(.*?)"'
    keyword = re.findall(pat, response, re.S)
    print(len(keyword))

    for hot_word in keyword:
        # 汉字不符合url标准，所以这里需要进行url编码
        i = urllib.parse.quote(hot_word, encoding='utf-8', errors='replace')
        # url构建
        link = f'https://www.baidu.com/s?cl=3&tn=baidutop10&fr=top1000&wd={i}&rsv_idx=2&rsv_dl=fyb_n_homepage&hisfilter=1'
        print(link)


def get_data2():
    # 发起请求
    html = requests.get('https://www.baidu.com/', headers=headers)
    html2 = html.content.decode('utf-8')
    doc = etree.HTML(html2)

    # 此时responses是一个list[]
    response = doc.xpath('//textarea [@id="hotsearch_data"]/text()')
    print(response)
    exit(234)

    # 此时遍历response得到item(item为字典类型)
    for item in response:
        # 通过key获取item的value----item2
        item2 = eval(item).get("hotsearch")  # 此处需要用eval智能识别item的类型
        # item2也是一个list,再次遍历得到item3
        for item3 in item2:
            # item3也是字典类型，通过key('pure_title')得到value
            print(item3.get('pure_title'))
