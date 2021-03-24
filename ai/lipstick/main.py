# encoding=utf-8

'''
圣罗兰
[('撩骚', '#D62352'), ('一见倾心', '#DC4B41'), ('浮生若梦', '#B22146'), ('纯真梦幻', '#A25356'), ('红粉派对', '#DF3443'), ('珊瑚恋人', '#E06C68'), ('华丽转身', '#842C71'), ('唇印', '#D13C4F'), ('危情禁果', '#B71D32'), ('情窦初开', '#DE2361'), ('裸色暗恋', '#B05856'), ('邂逅巴黎', '#E06F70'), ('糖果女孩', '#CD4143'), ('告白', '#EC6A70'), ('初恋', '#EFE9DE'), ('拥吻', '#C60F2F'), ('心跳', '#BB6868'), ('约定', '#E0186B'), ('游戏', '#D45E85'), ('意外', '#C16E6F'), ('钟情', '#D1121B'), ('夜色', '#8E243E'), ('私语', '#EE7486')]


香奈儿可可小姐
[('传情', '#F17365'), ('自由', '#E87268'), ('CORAIL RADIEUX', '#EA4D4A'), ('洒脱', '#D53D49'), ('水漾纱丽', '#FD4334'), ('倔强', '#E94648'), ('SHIPSHAPE', '#FF3220'), ('波希米亚', '#C12A33'), ('对白', '#CE1220'), ('冒险', '#EB6F79'), ('MIGHTY', '#EC5193'), ('卡柏男孩', '#D1918D'), ('传奇', '#E86A75'), ('勇敢', '#ED5A5E'), ('ROSE RAVISSANT', '#E93A5B'), ('约会', '#F8657F'), ('浪漫爱情', '#F14C77'), ('ENERGY', '#EB2755'), ('蒙特卡罗', '#E12948'), ('RENOUVEAU', '#E7394A'), ('率真', '#CC4D68'), ('安蒂岗妮', '#BB395F'), ('幸福时光', '#C54463')]


迪奥
[('鸡尾酒', '#EB636B'), ('泡泡堂', '#EB5C97'), ('小心计', '#E47082'), ('日光浴', '#EA5344'), ('购物狂', '#E94858'), ('混日子', '#C86378'), ('热点', '#E74218'), ('生存游戏', '#EA5331'), ('人生赢家', '#E60860'), ('可乐部', '#902216'), ('花蝴蝶', '#E51E1B'), ('天生玩家', '#95358C'), ('好莱坞大咖', '#A01314'), ('红酒', '#901A32'), ('给我迪奥', '#C4032B'), ('野蛮女友', '#BB0E63'), ('黑咖啡', '#391E1D'), ('不羁', '#602227')]


美宝莲
[('', '#99163A'), ('', '#A22040'), ('COLOR SENSATIONAL VIVID MATTE', '#C31431'), ('', '#EC5C80'), ('', '#EC594F'), ('', '#F193AD')]


纪梵希
[('优雅米色', '#DF695F'), ('迷人茶色', '#C74A52'), ('阳光小麦', '#A82A40'), ('幻想玫瑰', '#F43556'), ('樱桃玫瑰', '#BE2446'), ('加仑玫瑰', '#E70060'), ('加州红', '#F82131'), ('法式红', '#E50036'), ('珊瑚红', '#FA054B'), ('芭比红', '#FB2C60'), ('缪斯红', '#FA013D'), ('糖果玫瑰', '#FA6173'), ('明艳玫瑰', '#F60071'), ('大丽玫瑰', '#FF4D89'), ('覆盆子红', '#AC003A'), ('暖柿红', '#E03B35'), ('石榴红', '#93142F'), ('西瓜红', '#DF3751'), ('复古玫瑰', '#BB3C5A'), ('高雅梅', '#C53057'), ('勃艮第红', '#932844'), ('莓紫红', '#9B325A'), ('秀场红', '#EE4650'), ('圣水红', '#E11020'), ('橡皮裸肌', '#844452'), ('红色高跟鞋', '#731919'), ('复古提琴', '#64263F'), ('赤霞珠', '#58151E')]

'''

import face_recognition
import cv2
import numpy as np
from PIL import Image, ImageDraw


# 16进制颜色格式颜色转换为RGB格式
def Hex_to_RGB(hex):
    r = int(hex[1:3], 16)
    g = int(hex[3:5], 16)
    b = int(hex[5:7], 16)
    rgb = str(r) + ',' + str(g) + ',' + str(b)
    # print(rgb)
    return (r, g, b)


# def PutLipsticks(imgPath, hexcolor):
#     rgbcolor = Hex_to_RGB(hexcolor)
#     image = face_recognition.load_image_file(imgPath)
#     face_landmarks_list = face_recognition.face_landmarks(image)
#     # print(face_landmarks_list)
#     pil_image = Image.fromarray(image)
#     savePath = './static/{}'.format(imgPath.split('/')[-1])
#     for face_landmarks in face_landmarks_list:
#         d = ImageDraw.Draw(pil_image, 'RGB')
#         d.polygon(face_landmarks['top_lip'], fill=(rgbcolor[0],rgbcolor[1],rgbcolor[2]))
#         d.polygon(face_landmarks['bottom_lip'], fill=(rgbcolor[0],rgbcolor[1],rgbcolor[2]))
#     pil_image.save(savePath)
#     return savePath

def PutLipsticks(imgPath, hexcolor, index):
    rgbcolor = Hex_to_RGB(hexcolor)
    image = face_recognition.load_image_file(imgPath)
    face_landmarks_list = face_recognition.face_landmarks(image)
    # print(face_landmarks_list)
    pil_image = Image.fromarray(image)
    savePath = './static/{}.jpg'.format(index)
    for face_landmarks in face_landmarks_list:
        d = ImageDraw.Draw(pil_image, 'RGB')
        d.polygon(face_landmarks['top_lip'], fill=(rgbcolor[0], rgbcolor[1], rgbcolor[2]))
        d.polygon(face_landmarks['bottom_lip'], fill=(rgbcolor[0], rgbcolor[1], rgbcolor[2]))
    pil_image.save(savePath)
    return savePath


colors = ["#391E1D", "#FD4334", "#DF695F", "#E12948"]
for i in range(4):
    PutLipsticks("testpic/6.jpg", colors[i], i)
