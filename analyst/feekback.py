import jieba
"""
分词
lcut返回的结果是列表，而cut返回的是生成器
"""
str = '任性的90后boy来自于创新发展的大城市深圳史蒂夫，他曾经是个小渔村, 如今发展成了一个充满创新力城市'
aa = jieba.cut(str)
jieba.add_word('任性的')
jieba.add_word('来自于')
for y in aa:
    print(y, end=',')

ab = jieba.lcut(str, cut_all=True)
ab = '/' . join(ab)
print("\n", ab)
print(ab.count('城市'))