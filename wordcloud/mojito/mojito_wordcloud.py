# 1 导入相关库
import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from imageio import imread

import warnings

warnings.filterwarnings("ignore")

# 2 读取文本文件，并使用lcut()方法进行分词
with open("../data/dan_mu.txt", encoding="utf-8") as f:
    txt = f.read()
txt = txt.split()
data_cut = [jieba.lcut(x) for x in txt]

# 3 读取停用词
with open(r"../data/stop_list.txt", encoding="utf-8") as f:
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
# 1）读取背景图片
back_picture = imread(r"../data/img/china.png")

# 2）设置词云参数
wc = WordCloud(font_path="../../data/ttf/simhei.ttf",
               background_color="white",
               max_words=2000,
               mask=back_picture,
               max_font_size=200,
               random_state=42
               )
wc2 = wc.fit_words(word_count)

# 3）绘制词云图
plt.figure(figsize=(16, 8))
plt.imshow(wc2)
plt.axis("off")
plt.show()
wc.to_file("../data/temp/ciyun3.png")

