import threading
import time
import sys
import os

# 绝对路径
work_dir = os.path.dirname(os.path.abspath(__file__))
# 把当前路径切换到文件所在的路径
os.chdir(work_dir)

root_dir = '../../../'
sys.path.append(root_dir)
from lib.helper import Helper
from lib.sina import Sina
from lib.workwx import WeChat

# 获取stock配置
hp = Helper()
stock_config = hp.load_json_config('stock_config')


# 企业微信
def send_workwx_msg(content):
    wx = WeChat()
    wx.send_markdown(content)


def cron_run():
    t = threading.Timer(0, event_func)
    t.setDaemon(True)
    t.start()


def event_func():
    print('running')


# 判断交易日
def to_break():
    ts = time.time()
    t = time.localtime(ts)
    tt = time.strftime("%H:%M:%S", t)
    dayofweek = t.tm_wday
    # 周六周日不交易
    if dayofweek > 4:
        return True
    # 处于交易时间段
    if "09:25:00" < tt < "15:00:00":
        return False

    return True


# 循环获取每个stock 数据
def loop_stock(show_all=False):
    sina = Sina()
    stock_msg = ''
    for row in stock_config['codes']:
        print(f'loading......{row["code"]}')
        data = sina.get_stock_realtime(row['code'])
        # print(data)
        # exit()
        if row['rate'][0] < data['rate'] < row['rate'][1] and show_all is False:
            continue

        temp = "CO: {}，".format(row['code'].upper())
        temp += "昨: {}，".format(data['prev_price'])
        temp += "今: {}，".format(data['open_price'])
        temp += "实时: {}，".format(data['now_price'])
        temp += "高: {}，".format(data['max_price'])
        temp += "低: {}，".format(data['low_price'])
        temp += "量: {}万手，".format(data['deal_num'])
        # 涨跌幅
        if data['rate'] >= 0:  # 涨
            temp += "<font color=\"warning\">↑：{}%</font>，ZH: {}\n""".format(
                format(data['rate'], '.2f'), data['name'])
        elif data['rate'] < 0:  # 跌
            temp += "<font color=\"info\">↓：{}%</font>，ZH: {}\n""".format(
                format(data['rate'], '.2f'), data['name'])
        else:
            temp = """<font color=\"comment\">failed！！</font>\n""".format(data['code'])
        stock_msg += temp

    body_content = "<font color=\"comment\">Sina Stock's Report. {}</font>\n".format(
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    body_content += stock_msg
    body_content += "\n<font color=\"comment\">[The stock market is risky, investment needs to be cautious]</font>"
    return body_content


def main():
    cont = loop_stock(show_all=True)
    # print(cont)
    WeChat().send_markdown(cont)


if __name__ == '__main__':
    main()
