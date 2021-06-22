"""
助手函数方法
"""
import os
import json
import requests
import smtplib
import hashlib
# 负责构造文本
from email.mime.text import MIMEText
# 负责构造图片
# 负责将多个对象集合起来
from email.mime.multipart import MIMEMultipart
from email.header import Header


class Helper:

    # 加载配置
    @staticmethod
    def load_json_config(file_name):
        with open('../data/config/{}.json'.format(file_name), 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config

    # requests.get
    @staticmethod
    def get_common_url(url, params=None, headers=None, proxies=None):
        rsp = requests.get(url, params=params, headers=headers, proxies=proxies)
        rsp.raise_for_status()
        return rsp.text

    # 保留n位小数, 四舍五入
    @staticmethod
    def float_format(num, decimals=2):
        """
        num: 浮点数
        decimals: 保留小数位数
        """
        str_num = str(num)
        a1, b1, c1 = str_num.partition('.')
        if len(c1) > decimals:
            cc = c1[:decimals]
            if int(c1[decimals]) >= 5:
                ccc = int(cc) + 1
            else:
                ccc = int(cc)
            if cc[0] == '0':
                ccc = cc[0] + str(ccc)
        else:
            ccc = c1
        return float(a1 + b1 + str(ccc))

    # 发送邮件
    @staticmethod
    def send_mail(content, receiver_mail, thresh=1, user=None):
        """
        content：发送内容
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
        # 构造文本,参数1：正文内容，参数2：文本格式，参数3：编码方式
        message_text = MIMEText(content, "plain", "utf-8")
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
        # print("邮件发送成功")
        # 关闭SMTP对象
        stp.quit()

    @staticmethod
    def get_md5(file_path):
        f = open(file_path, 'rb')
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        md5_hash = md5obj.hexdigest()
        f.close()
        return str(md5_hash).upper()

    # 过滤同级目录下的重复文件
    def filter_repeat_file(self):
        path = input("请输入需要重复文件过滤文件夹路径：")
        file_list = os.listdir(path)
        file_md5 = []
        for filename in file_list:
            md5val = self.get_md5(path + filename)
            if md5val in file_md5:
                print('重复文件：' + path + filename)
                # os.remove(path + filename)
            else:
                file_md5.append(md5val)
        print("处理完毕...")


if __name__ == '__main__':
    hp = Helper()
    hp.filter_repeat_file()
