import requests
import urllib3

url = 'https://xueqiu.com/'
headers = {
    'Host': 'xueqiu.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
}

proxies = {}

# 移除因移除SSL认证出现的警告
urllib3.disable_warnings()
resp = requests.get(url, headers=headers, verify=True, proxies=proxies)
if resp.status_code == 200:
    html_bytes = resp.content
    html_str = html_bytes.decode()
    print(html_str)
else:
    print(f'errno-{resp.status_code}')
