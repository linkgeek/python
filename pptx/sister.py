'''
星座运势PPT
'''

import json
import time
import requests
import pandas as pd
from pptx import Presentation
from pptx.util import Pt, Inches
from pptx.enum.text import MSO_ANCHOR
from pptx.dml.color import RGBColor  # add this import to the top of the file
from bs4 import BeautifulSoup as BS


class ConstellationPPT(object):

    def __init__(self):
        self.appkey = "your_token"
        self.data = pd.read_csv("../data/totalData.csv", encoding="gbk")
        self.results = {i: [] for i in self.data["names"].values.tolist()}
        self.keys = {i: j for i, j in self.data[["names", "constellations"]].values}
        self.setCons = {i: [] for i in set(self.keys.values())}
        self.pres = Presentation()
        self.headers = ''
        self.constellationUrl = ''
        self.totalData = []

    def getConstellations(self):
        resp = requests.get(self.constellationUrl, headers=self.headers)
        resp.encoding = 'utf-8'
        text = resp.text
        soup = BS(text, 'lxml')
        pstext = [p.text for p in soup.find('div', {'class', 'topic-richtext'}).find_all("p")]
        for ptext in pstext:
            constellation, names = ptext.splite(":")
            for name in names.split(" "):
                self.totalData[name].append(constellation)

    def saveData(self):
        data = self.totalData.values()
        names = list(self.totalData.keys())
        picurls = [i[0] for i in data]
        constellations = [i[1] for i in data]
        pd.DataFrame({"name": names, "picurls": picurls, "constellations": constellations}).to_cvs('totalData.csv', index_label="index_label")


    def GetResult(self):
        url = "http://web.juhe.cn:8080/constellation/getAll"
        for i in self.results.keys():
            print(i)
            if self.setCons[self.keys[i]]:
                self.results[i].extend(self.setCons[self.keys[i]])
            else:
                params = {
                    "key": self.appkey,  # 应用APPKEY(应用详细页查询)
                    "consName": self.keys[i],  # 星座名称，如:白羊座
                    "type": "tomorrow",  # 运势类型：today,tomorrow,week,nextweek,month,year
                }
                content = requests.get(url, params=params).text
                res = json.loads(content)
                if res:
                    error_code = res["error_code"]
                    if error_code == 0:
                        temp = [res["name"], res["datetime"], res["all"], res["color"], res["number"], res["summary"]]
                        self.results[i].extend(temp)
                        self.setCons[self.keys[i]] = temp
                    else:
                        print("%s:%s" % (res["error_code"], res["reason"]))
                else:
                    print("request api error")
            time.sleep(2)

    def AddSlide(self):
        # self.GetResult()  # 将星座运势信息写入到self.results字典中去：{"伊能静":[幸运色、幸运数字...],"黄圣依":[幸运色、幸运数字...] }
        self.results = {'许飞': ['天蝎座', '2020年07月01日', '80', '绿色', 3,
                               '今天天蝎们在人际关系上比较有利，沟通交流或是外出办事都比较顺利。不过还是有可能出现计划之外的情况。部分天蝎今天会萌生旅行的想法，也有天蝎们今天会因为心情的原因就疯狂网购。'],
                        '万茜': ['金牛座', '2020年07月01日', '80', '咖啡色', 0,
                               '今天牛牛们要注意下健康和财务问题。健康上容易上火长东西或是出血之类（也容易失眠）。财务上今天容易有些不必要的花销，另外也不要听人忽悠投资。今天在工作上牛牛们能得到领导的支持，不过领导可能会不太明确工作方向，要确认清楚。'],
                        '伊能静': ['双鱼座', '2020年07月01日', '80', '白色', 1,
                                '今天双鱼们要注意下感情。最近双鱼们的想法有些游移不定，不太清楚自己究竟要什么，这让对方不知道该怎么相处。人际方面，双鱼们今天可能会觉得自己没有被朋友重视。'],
                        '袁咏琳': ['天蝎座', '2020年07月01日', '80', '绿色', 3,
                                '今天天蝎们在人际关系上比较有利，沟通交流或是外出办事都比较顺利。不过还是有可能出现计划之外的情况。部分天蝎今天会萌生旅行的想法，也有天蝎们今天会因为心情的原因就疯狂网购。'],
                        '张萌': ['双鱼座', '2020年07月01日', '80', '白色', 1,
                               '今天双鱼们要注意下感情。最近双鱼们的想法有些游移不定，不太清楚自己究竟要什么，这让对方不知道该怎么相处。人际方面，双鱼们今天可能会觉得自己没有被朋友重视。'],
                        '黄圣依': ['水瓶座', '2020年07月01日', '80', '红色', 2,
                                '今天水瓶们可能会觉得精神压力有些大，部分水瓶也会失眠。在工作上今天可能会需要加班，也需要帮领导处理一些杂事。水瓶们今天或许会有些赚钱的想法，不过目前还拿不定主意。'],
                        '孟佳': ['水瓶座', '2020年07月01日', '80', '红色', 2,
                               '今天水瓶们可能会觉得精神压力有些大，部分水瓶也会失眠。在工作上今天可能会需要加班，也需要帮领导处理一些杂事。水瓶们今天或许会有些赚钱的想法，不过目前还拿不定主意。'],
                        '王智': ['狮子座', '2020年07月01日', '80', '白色', 4,
                               '狮子们今天要注意财务的花销。部分狮子可能会因为工作原因垫付款项，也有狮子会在健康上有支出。狮子们今天想法虽然很多，但是不太想与人交流。部分狮子今天会参加聚会，不过期间可能会发生一些让自己不开心的事。'],
                        '王霏霏': ['金牛座', '2020年07月01日', '80', '咖啡色', 0,
                                '今天牛牛们要注意下健康和财务问题。健康上容易上火长东西或是出血之类（也容易失眠）。财务上今天容易有些不必要的花销，另外也不要听人忽悠投资。今天在工作上牛牛们能得到领导的支持，不过领导可能会不太明确工作方向，要确认清楚。'],
                        '金莎': ['双鱼座', '2020年07月01日', '80', '白色', 1,
                               '今天双鱼们要注意下感情。最近双鱼们的想法有些游移不定，不太清楚自己究竟要什么，这让对方不知道该怎么相处。人际方面，双鱼们今天可能会觉得自己没有被朋友重视。'],
                        '张雨绮': ['狮子座', '2020年07月01日', '80', '白色', 4,
                                '狮子们今天要注意财务的花销。部分狮子可能会因为工作原因垫付款项，也有狮子会在健康上有支出。狮子们今天想法虽然很多，但是不太想与人交流。部分狮子今天会参加聚会，不过期间可能会发生一些让自己不开心的事。'],
                        '张含韵': ['白羊座', '2020年07月01日', '80', '绿色', 3,
                                '今天白羊们在工作上比较有自己的想法或是规划，也有白羊会接受领导新派的任务或是给予的支持。不过要注意的是，今天在工作计划安排上容易变动，领导的想法也摇摆不定。今天也要注意与同事的关系处理，对方有些大嘴巴。今天在健康上也容易上火。'],
                        '朱婧汐': ['白羊座', '2020年07月01日', '80', '绿色', 3,
                                '今天白羊们在工作上比较有自己的想法或是规划，也有白羊会接受领导新派的任务或是给予的支持。不过要注意的是，今天在工作计划安排上容易变动，领导的想法也摇摆不定。今天也要注意与同事的关系处理，对方有些大嘴巴。今天在健康上也容易上火。'],
                        '刘芸': ['摩羯座', '2020年07月01日', '80', '红色', 2,
                               '今天部分人会有出行的安排，不过可能又会临时改期。今天也是适宜处理人际关系的日子。部分摩羯可能需要帮领导处理一些文案方面的事，也有人要去拜访重点客户。今天和朋友或是另一半聚会也是不错的选择，不过摩羯们可能会觉得对方有些冷淡。'],
                        '阿朵': ['白羊座', '2020年07月01日', '80', '绿色', 3,
                               '今天白羊们在工作上比较有自己的想法或是规划，也有白羊会接受领导新派的任务或是给予的支持。不过要注意的是，今天在工作计划安排上容易变动，领导的想法也摇摆不定。今天也要注意与同事的关系处理，对方有些大嘴巴。今天在健康上也容易上火。'],
                        '白冰': ['金牛座', '2020年07月01日', '80', '咖啡色', 0,
                               '今天牛牛们要注意下健康和财务问题。健康上容易上火长东西或是出血之类（也容易失眠）。财务上今天容易有些不必要的花销，另外也不要听人忽悠投资。今天在工作上牛牛们能得到领导的支持，不过领导可能会不太明确工作方向，要确认清楚。'],
                        '李斯丹妮': ['金牛座', '2020年07月01日', '80', '咖啡色', 0,
                                 '今天牛牛们要注意下健康和财务问题。健康上容易上火长东西或是出血之类（也容易失眠）。财务上今天容易有些不必要的花销，另外也不要听人忽悠投资。今天在工作上牛牛们能得到领导的支持，不过领导可能会不太明确工作方向，要确认清楚。'],
                        '钟丽缇': ['处女座', '2020年07月01日', '80', '蓝色', 1,
                                '整体运势处于严峻的形势中，卑微的姿态会让你委屈求全。你会低估自己的实力，总是膜拜和羡慕别人的才能，却没有看到自己身上也有发光点。所以在选择上你会服从别人的安排，或是将机会拱手让人，就是不相信自己也能行。'],
                        '吴昕': ['水瓶座', '2020年07月01日', '80', '红色', 2,
                               '今天水瓶们可能会觉得精神压力有些大，部分水瓶也会失眠。在工作上今天可能会需要加班，也需要帮领导处理一些杂事。水瓶们今天或许会有些赚钱的想法，不过目前还拿不定主意。'],
                        '宁静': ['金牛座', '2020年07月01日', '80', '咖啡色', 0,
                               '今天牛牛们要注意下健康和财务问题。健康上容易上火长东西或是出血之类（也容易失眠）。财务上今天容易有些不必要的花销，另外也不要听人忽悠投资。今天在工作上牛牛们能得到领导的支持，不过领导可能会不太明确工作方向，要确认清楚。'],
                        '蓝盈莹': ['白羊座', '2020年07月01日', '80', '绿色', 3,
                                '今天白羊们在工作上比较有自己的想法或是规划，也有白羊会接受领导新派的任务或是给予的支持。不过要注意的是，今天在工作计划安排上容易变动，领导的想法也摇摆不定。今天也要注意与同事的关系处理，对方有些大嘴巴。今天在健康上也容易上火。'],
                        '郑希怡': ['处女座', '2020年07月01日', '80', '蓝色', 1,
                                '整体运势处于严峻的形势中，卑微的姿态会让你委屈求全。你会低估自己的实力，总是膜拜和羡慕别人的才能，却没有看到自己身上也有发光点。所以在选择上你会服从别人的安排，或是将机会拱手让人，就是不相信自己也能行。'],
                        '黄龄': ['水瓶座', '2020年07月01日', '80', '红色', 2,
                               '今天水瓶们可能会觉得精神压力有些大，部分水瓶也会失眠。在工作上今天可能会需要加班，也需要帮领导处理一些杂事。水瓶们今天或许会有些赚钱的想法，不过目前还拿不定主意。'],
                        '王丽坤': ['白羊座', '2020年07月01日', '80', '绿色', 3,
                                '今天白羊们在工作上比较有自己的想法或是规划，也有白羊会接受领导新派的任务或是给予的支持。不过要注意的是，今天在工作计划安排上容易变动，领导的想法也摇摆不定。今天也要注意与同事的关系处理，对方有些大嘴巴。今天在健康上也容易上火。'],
                        '郁可唯': ['天秤座', '2020年07月01日', '75', '咖啡色', 0,
                                '今天在工作上团队内部不太和谐，可能会出现同事互相推诿的情况。工作计划也难以明确。今天天秤们也要注意处理与家人之间的关系，也有天秤们在涉及房屋的事务上反复纠结或是房子出现小毛病。健康上今天容易失眠。'],
                        '丁当': ['白羊座', '2020年07月01日', '80', '绿色', 3,
                               '今天白羊们在工作上比较有自己的想法或是规划，也有白羊会接受领导新派的任务或是给予的支持。不过要注意的是，今天在工作计划安排上容易变动，领导的想法也摇摆不定。今天也要注意与同事的关系处理，对方有些大嘴巴。今天在健康上也容易上火。'],
                        '金晨': ['处女座', '2020年07月01日', '80', '蓝色', 1,
                               '整体运势处于严峻的形势中，卑微的姿态会让你委屈求全。你会低估自己的实力，总是膜拜和羡慕别人的才能，却没有看到自己身上也有发光点。所以在选择上你会服从别人的安排，或是将机会拱手让人，就是不相信自己也能行。'],
                        '海陆': ['天秤座', '2020年07月01日', '75', '咖啡色', 0,
                               '今天在工作上团队内部不太和谐，可能会出现同事互相推诿的情况。工作计划也难以明确。今天天秤们也要注意处理与家人之间的关系，也有天秤们在涉及房屋的事务上反复纠结或是房子出现小毛病。健康上今天容易失眠。'],
                        '陈松伶': ['水瓶座', '2020年07月01日', '80', '红色', 2,
                                '今天水瓶们可能会觉得精神压力有些大，部分水瓶也会失眠。在工作上今天可能会需要加班，也需要帮领导处理一些杂事。水瓶们今天或许会有些赚钱的想法，不过目前还拿不定主意。'],
                        '沈梦辰': ['双子座', '2020年07月01日', '80', '白色', 4,
                                '今天双子们可能会遇到想法不定的领导，也有人会接到一个模拟两可的任务。部分双子今天会有理财或是健康咨询之类的想法。今天也有可能会需要为工作垫款。双子们今天也会特别关注形象方面的事。']}
        for item in self.results.items():  # 对每一个小姐姐的信息
            slide = self.pres.slides.add_slide(self.pres.slide_layouts[5])  # 添加空白页PPT，样式为只有一个文本框
            body_shape = slide.shapes.placeholders  # 获取空白页中的初始文本框
            body_shape[0].text = '{}今日星座运势'.format(item[0])  # 在第一个文本框中文字框架内添加文字
            left, top, width, height = Inches(4), Inches(2), Inches(5), Inches(5)  # 设置新文本框的位置和大小。
            text = ["星座：{}".format(item[1][0]), "时间：{}".format(item[1][1]), "综合指数:{}".format(item[1][2]),
                    "幸运色:{}".format(item[1][3]), "幸运数字：{}".format(item[1][4]),
                    "今日概述：{}".format(item[1][5])]
            textbox = slide.shapes.add_textbox(left, top, width, height)  # left，top为相对位置，width，height为文本框大小
            textbox.text = text[0]  # 文本框中文字
            for i in text[1:]:  # 分别写入时间，综合指数，幸运色。。。
                tf = textbox.text_frame
                tf.add_paragraph().text = i
                tf.add_paragraph().font.color.rgb = RGBColor(255, 255, 0)
                tf.vertical_anchor = MSO_ANCHOR.BOTTOM  # 对齐文本方式：底端对齐
                tf.word_wrap = True  # 自动换行

            img_path = '../data/girls/{}.jpg'.format(item[0])  # 图片文件路径名称
            img_url = 'https://bkimg.cdn.bcebos.com/pic/f703738da9773912b31b1f61b8509118367adab444d3?x-bce-process=image'
            img_cont = requests.get(img_url)
            # 图片二进制
            img_er = img_cont.content
            # 保存图片
            with open(img_path, 'wb') as file:
                file.write(img_er)
                file.flush()

            left, top, width, height = Inches(1), Inches(2.5), Inches(2), Inches(2)  # 设置图片放置的位置和大小
            slide.shapes.add_picture(img_path, left, top, width, height)  # 在指定位置按预设值添加图片
        self.pres.save('../data/乘风破浪.pptx')  # 保存PPT


if __name__ == '__main__':
    consPPT = ConstellationPPT()
    consPPT.AddSlide()
