import smtplib
import email
# 负责构造文本
from email.mime.text import MIMEText
# 负责构造图片
from email.mime.image import MIMEImage
# 负责将多个对象集合起来
from email.mime.multipart import MIMEMultipart
from email.header import Header

import requests
from bs4 import BeautifulSoup
import re
import time

import sys

sys.path.append('..')
from api.workwx import WeChat

fund_codes = []

# 获取stock 列表
def share_code():
    with open('./fund_code.txt', 'r') as file:
        print(file.readlines())
        exit()
        for code in file.readlines():
            fund_codes.append(code.strip())


# 获取基金涨跌
def get_fund_info(fund_code):
    """
    获取基金涨跌幅信息：信息来源（新浪财经 http://stocks.sina.cn/fund/）
    fund_code：为基金代码，若该基金不存在，返回 False，否则返回 涨跌幅比例
    """
    headers = {
        "Cookie": 'ustat=__14.28.56.65_1590560309_0.89300000; genTime=1590560309; SINAGLOBAL=4905578110989.475.1590560312465; Apache=3574138427052.4756.1595941642394; ULV=1595941642397:5:2:1:3574138427052.4756.1595941642394:1594733801049; sinaH5EtagStatus=y; vt=99; historyRecord={"href":"http://stocks.sina.cn/fund/","refer":""}',
        "Host": "stocks.sina.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
    }
    url = url = "http://stocks.sina.cn/fund/?code={}&vt=4#".format(fund_code)
    try:
        r = requests.get(url, headers)
        r.encoding = "UTF-8"
        soup = BeautifulSoup(r.text, "html.parser")
        result = soup.findAll(attrs={"class": "j_fund_valExt"})
        if len(result) == 1:
            pattern = "(?<=>)(.+)(?=<)"
            result = re.findall(pattern, str(result[0]))[0]
            return float(result.split("%")[0])
        else:
            return False
    except:
        return False


# 生成发送内容
def gen_cont(fund_code, thresh):
    body_content = "时间：{} \n\n".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    for code in fund_code:
        rate = get_fund_info(code)
        # print(code, rate)
        # exit()
        # 邮件正文内容
        if rate:
            #####  根据基金代码获取基金信息
            headers = {
                "Cookie":
                    "qgqp_b_id=f8b59df051caea02b176f6d76db75887; EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=null; EMFUND7=null; st_si=92310565820236; st_asi=delete; searchbar_code=160119; EMFUND0=null; EMFUND8=07-14%2021%3A54%3A31@%23%24%u5357%u65B9%u4E2D%u8BC1500ETF@%23%24510500; EMFUND9=07-25 23:07:36@#$%u5357%u65B9%u4E2D%u8BC1500ETF%u8054%u63A5A@%23%24160119; ASP.NET_SessionId=5ljqqn1s20zpfryhuw5fx4jw; st_pvi=06954122844047; st_sp=2020-05-20%2007%3A32%3A46; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=2; st_psi=20200725230736417-0-5210348614",
                "User-Agent":
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
            }
            url = "http://fund.eastmoney.com/js/fundcode_search.js"
            r = requests.get(url, headers)
            info = re.findall("(\[.*?\])", r.text[9:-2])
            fund_info = \
                list(filter(lambda x: x.replace("\"", "").replace("[", "").replace("]", "").split(",")[0] == code,
                            info))[0]

            if abs(rate) > thresh:
                temp = """{} 基金 \n 涨幅为 {}%, \n \t \t ### 涨跌幅超过阈值！！！ ### \n\n""".format(fund_info, rate)
            else:
                temp = """{} 基金 \n 涨幅为 {}% \n\n""".format(fund_info, rate)
        else:
            temp = """{} 基金 \n 获取失败！！！""".format(code)
        body_content += temp

    body_content = "【股市有风险，投资需谨慎】"
    return body_content


# 发送邮件
def send_mail(fund_code, receiver_mail, thresh=1, user=None):
    """
    fund_code：基金代码
    receiver_mail：收件人邮箱
    thresh：阈值
    user：用户名标志
    """
    # SMTP服务器,这里使用qq邮箱
    mail_host = "smtp.qq.com"
    # 发件人邮箱
    mail_sender = "xxx@qq.com"
    # 邮箱授权码
    mail_license = "xxxxx"

    # 收件人邮箱，可以为多个收件人
    mail_receivers = [receiver_mail]  # ["******@qq.com","******@foxmail.com"]
    # print(mail_receivers)
    # 构建 MIMEMultipart 对象代表邮件本身，可以往里面添加文本、图片、附件等
    mm = MIMEMultipart('related')

    # 邮件主题
    subject_content = """基金"""
    # 设置发送者,注意严格遵守格式,里面邮箱为发件人邮箱
    mm["From"] = "sender_name<xxx@qq.com>"
    # 设置接受者,注意严格遵守格式,里面邮箱为接受者邮箱
    # 多个接受者 "receiver_1_name<******@qq.com>,receiver_2_name<******@foxmail.com>"
    mm["To"] = "receiver_1_name<{}>".format(receiver_mail)
    # 设置邮件主题
    mm["Subject"] = Header(subject_content, 'utf-8')
    body_content = gen_cont(thresh)
    # 构造文本,参数1：正文内容，参数2：文本格式，参数3：编码方式
    message_text = MIMEText(body_content, "plain", "utf-8")
    # 向MIMEMultipart对象中添加文本对象
    mm.attach(message_text)

    # 创建SMTP对象
    stp = smtplib.SMTP()
    # 设置发件人邮箱的域名和端口，端口地址为25
    stp.connect(mail_host, 25)
    # set_debuglevel(1)可以打印出和SMTP服务器交互的所有信息
    stp.set_debuglevel(0)

    # 登录邮箱，传递参数1：邮箱地址，参数2：邮箱授权码
    stp.login(mail_sender, mail_license)
    # 发送邮件，传递参数1：发件人邮箱地址，参数2：收件人邮箱地址，参数3：把邮件内容格式改为str
    stp.sendmail(mail_sender, mail_receivers, mm.as_string())
    print("邮件发送成功")
    # 关闭SMTP对象
    stp.quit()


# 发送企业微信
def send_workwx_msg(content):
    wx = WeChat()
    # wx.send_data("这是程序发送的第1条消息！\n Python程序调用企业微信API！")
    wx.send_data(content)


def main():
    share_code()
    print(fund_codes)
    exit()
    content = gen_cont(fund_codes, 1)
    print(content)
    exit()
    send_workwx_msg(content)
    # send_mail(fund_code=fund_code, receiver_mail="xxxxx@foxmail.com", thresh=1, user="LSJ")


if __name__ == '__main__':
    main()
