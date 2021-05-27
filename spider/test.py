import requests
import urllib3

url = 'https://www.btbw.xyz/list.php?class=guochan&page=1'
headers = {
    # 'Host': 'btbw.xyz',
    'authority': 'www.btbw.xyz',
    'method': 'GET',
    'path': '/list.php?class=guochan',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': '_ga=GA1.1.1947293559.1621949576; cf_clearance=e44314b49a81e7dbafe935bdb5f74efe2acd8f6f-1621955693-0-250; _ga_Q3P79YL0DW=GS1.1.1622037355.3.1.1622039236.0',

    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
}

proxies = {}

# 移除因移除SSL认证出现的警告
urllib3.disable_warnings()
resp = requests.get(url, headers=headers, verify=False)
if resp.status_code == 200:
    html_bytes = resp.content
    html_str = html_bytes.decode()
    print(html_str)
else:
    print(f'errno-{resp.status_code}')
