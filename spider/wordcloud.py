
import wordcloud #导入词云库
import numpy as np
import matplotlib.pyplot as plt
import PIL
import jieba
import re
with open(r'E:\master\txt1.txt',encoding='utf8') as f:
    text1 = f.readlines()
#导入图片
image1 = PIL.Image.open(r'E:\master\picture.jpg')
MASK = np.array(image1)
WC = wordcloud.WordCloud(font_path = 'C:\\Windows\\Fonts\\STFANGSO.TTF',max_words=2000,mask = MASK,height= 400,width=400,background_color='white',repeat=False,mode='RGBA') #设置词云图对象属性
st1 = re.sub('[，。、“”‘ ’]','',str(text1)) #使用正则表达式将符号替换掉。
conten = ' '.join(jieba.lcut(st1)) #此处分词之间要有空格隔开，联想到英文书写方式，每个单词之间都有一个空格。
con = WC.generate(conten)
plt.imshow(con)
plt.axis("off")