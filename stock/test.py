import requests
import threading
import sys
sys.path.append('..')
from api.workwx import WeChat

code_list = []

# 获取stock 列表
def share_code():
    with open('../data/code_list.txt', 'r') as file:
        for code in file.readlines():
            code_list.append(code.strip())
    # print(code_list)

# 获取stock 数据
def get_stock(code, up_rate):
    url = 'http://hq.sinajs.cn/list=' + code
    r = requests.get(url)
    res = r.text
    # print(res)
    # var hq_str_sz000725 = "京东方Ａ,7.330,7.260,7.320,7.480,7.220,7.320,7.330,839689831,6173688383.270,1
    # 768566, 7.320, 2015100, 7.310, 2700200, 7.300, 737100, 7.290, 1054400, 7.280, 370800, 7.330, 4124140, 7.340, 3558400, 7.350, 5271880, 7.360, 3972600, 7.370, 2021 - 04 - 30, 14: 48:36, 00
    # ";

    result = res.split('=')[1]
    # 股票名称
    name = result.split(',')[0].replace('"', '')
    # 昨日收盘价
    start_price = float(result.split(',')[2])
    # 当前价格
    now_price = float(result.split(',')[3])
    # 涨跌幅度
    rate = (now_price - start_price) / start_price * 100

    content = ''
    if abs(rate) > up_rate:
        content = "股票预警：当前股票[{0}], 涨幅[{1:.2f}%], 请查收！【股票有风险，投资需谨慎】".format(name, rate)
    return content

# 循环获取每个stock 数据
def loop_stock(up_rate):
    share_code()
    for code in code_list:
        cont = get_stock(code, up_rate)
        if cont == '':
            continue

        #print(cont)
        send_workwx_msg(cont)

# 钉钉机器人
def send_dingding_msg(content):
    # content: 发送内容
    # isAtAll: 是否要@某位用户
    json_data = {"msgtype": "text", "text": {"content": content}, "at": {"atMobiles": [], "isAtAll": False}}
    ding_url = 'https://oapi.dingtalk.com/robot/send?access_token=dfb241394310aeb3a94d32f1b359b7382429f4b435f9f0eb605979f50b21e857'
    #requests.post(url=ding_url, json=json_data)
    print('预警信息发送成功!')

# 企业微信
def send_workwx_msg(content):
    wx = WeChat()
    #wx.send_data("这是程序发送的第1条消息！\n Python程序调用企业微信API！")
    wx.send_data(content)

def cron_run():
    t = threading.Timer(0, event_func)
    t.setDaemon(True)
    t.start()

def event_func():
    print('running')

def main():
    # get_stock('sz', '000725')
    up_rate = 1
    #loop_stock(up_rate)
    cron_run()


if __name__ == '__main__':
    main()
