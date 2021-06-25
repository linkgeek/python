# 天天基金股吧、贴吧
# https://blog.csdn.net/weixin_38753213/article/details/115610433
"""
pip install ipython
"""
import pandas as pd
import numpy as np
import jieba
import stylecloud
from IPython.display import Image

df = pd.read_csv("./161725.csv",
                 names=['阅读', '评论', '标题', '作者', '时间'])

# 重复和缺失数据
df = df.drop_duplicates()
df = df.dropna()

# 数据类型转换
df['阅读'] = df['阅读'].str.replace('万', '').astype('float')
df['时间'] = pd.to_datetime(df['时间'], errors='ignore')


# 机械压缩去重
def yasuo(st):
    for i in range(1, int(len(st) / 2) + 1):
        for j in range(len(st)):
            if st[j:j + i] == st[j + i:j + 2 * i]:
                k = j + i
                while st[k:k + i] == st[k + i:k + 2 * i] and k < len(st):
                    k = k + i
                st = st[:j] + st[k:]
    return st


yasuo(st="J哥J哥J哥J哥J哥")
df["标题"] = df["标题"].apply(yasuo)

# 过滤表情
df['标题'] = df['标题'].str.extract(r"([\u4e00-\u9fa5]+)")
df = df.dropna()  # 纯表情直接删除

# 过滤短句
df = df[df["标题"].apply(len) >= 3]
df = df.dropna()
print(df)

# 绘制词云图
text1 = get_cut_words(content_series=df['标题'])
stylecloud.gen_stylecloud(text=' '.join(text1), max_words=200,
                          collocations=False,
                          font_path='simhei.ttf',
                          icon_name='fas fa-heart',
                          size=653,
                          #palette='matplotlib.Inferno_9',
                          output_name='./基金.png')
Image(filename='./基金.png')


# 获取贴吧数据
def main():
    fund_code = 161725


if __name__ == '__main__':
    main()
