# 1 导入相关库
import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from imageio import imread
import warnings

warnings.filterwarnings("ignore")

# 2 读取文本文件，并使用lcut()方法进行分词
with open("dan_mu.txt", encoding="utf-8") as f:
    txt = f.read()
txt = txt.split()
data_cut = [jieba.lcut(x) for x in txt]

# 3 读取停用词
with open(r"stoplist.txt", encoding="utf-8") as f:
    stop = f.read()
stop = stop.split()
stop = [" ", "道", "说道", "说"] + stop

# 4 去掉停用词之后的最终词
s_data_cut = pd.Series(data_cut)
all_words_after = s_data_cut.apply(lambda x: [i for i in x if i not in stop])

# 5 词频统计
all_words = []
for i in all_words_after:
    all_words.extend(i)
word_count = pd.Series(all_words).value_counts()

# 6 词云图的绘制
# 6-1）读取背景图片
back_picture = imread(r"heart_bg.jpg")

# 6-2）设置词云参数
wc = WordCloud(font_path="simhei.ttf",  # 设置字体
               background_color="white",  # 背景颜色
               max_words=2000,  # 词云显示的最大词数
               mask=back_picture,  # 造型遮盖
               max_font_size=200,  # 字体最大值
               # min_font_size=20,  # 字体最小值
               random_state=42,  # 随机数
               collocations=False,  # 避免重复单词
               width=1600, height=1200, margin=10,  # 图像宽高，字间距，需要配合下面的plt.figure(dpi=xx)缩放才有效
              )
wc2 = wc.fit_words(word_count)

# 6-3）绘制词云图
plt.figure(figsize=(16, 8))
# plt.figure(figsize=(a, b), dpi=dpi) figsize设置图形的大小，a为图形的宽，b为图形的高，单位为英寸；dpi为设置图形每英寸的点数
plt.imshow(wc2)
plt.axis("off")  # 隐藏坐标
plt.show()
wc.to_file("heart2.png")