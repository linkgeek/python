"""
单纯的人像动漫化，不为人像戴口罩
"""

import requests, base64
import matplotlib.pyplot as plt  # plt 用于显示图片
import matplotlib.image as mpimg  # mpimg 用于读取图片
from PIL import Image


# 这个函数的操作是为了获取access_token参数
def get_access_token():

    data = {
        'grant_type': 'client_credentials',  # 固定值
        'client_id': 'giFiN1wphxIY8lIosxMD0DMd',  # 在开放平台注册后所建应用的API Key
        'client_secret': 'M1yNChTkokPqqsaw4mmqajtn9QOS1u5o'  # 所建应用的Secret Key
    }
    url = 'https://aip.baidubce.com/oauth/2.0/token'
    res = requests.post(url, data=data)
    res = res.json()
    # print(res)

    access_token = res['access_token']
    return access_token


def create_comic():

    request_url = "https://aip.baidubce.com/rest/2.0/image-process/v1/selfie_anime"
    f = open('girl2.jpg', 'rb')  # 二进制方式打开图片文件
    img = base64.b64encode(f.read())  # 图像转为base64的格式

    params = {"image": img}
    request_url = request_url + "?access_token=" + get_access_token()
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    res = response.json()

    # 前面我们讲述了这个请求返回的是一个字典，其中一个键就是image，代表的是处理后的图像信息
    # 将这个图像信息写入，得到最终的效果图
    if res:
        f = open("lu.jpg", 'wb')
        after_img = res['image']
        after_img = base64.b64decode(after_img)
        f.write(after_img)
        f.close()

        im = Image.open('lu.jpg')
        im.show()


if __name__ == '__main__':
    create_comic()
