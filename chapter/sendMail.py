import smtplib
from email.mime.image import MIMEImage  # 图片类型邮件
from email.mime.text import MIMEText  # MIME 多用于邮件扩充协议
from email.mime.multipart import MIMEMultipart  # 创建附件类型

HOST = 'smtp.qq.com'  # 调用的邮箱借借口
SUBJECT = '发送了一封Python SMTP 邮件测试'  # 设置邮件标题
FROM = '941192051@qq.com'  # 发件人的邮箱需先设置开启smtp协议
TO = '2387989495@qq.com'  # 设置收件人的邮箱（可以一次发给多个人,用逗号分隔）
CODE = 'vasmmsaspjoebbda'
# message = MIMEMultipart('related')  # 邮件信息，内容为空  #相当于信封##related表示使用内嵌资源的形式，将邮件发送给对方

# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
message['From'] = '加藤非'     # 发送者
message['To'] = '船长哈哈哈'   # 接收者
message['Subject'] = SUBJECT


def sendmail(HOST, FROM, TO, CODE, message):
    try:
        smtpObj = smtplib.SMTP(HOST)
        smtpObj.login(FROM, CODE)
        smtpObj.sendmail(FROM, TO, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


if __name__ == '__main__':
    sendmail(HOST=HOST, FROM=FROM, TO=TO, CODE=CODE, message=message)