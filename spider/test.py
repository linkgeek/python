import urllib.request #引入urllib库

response = urllib.request.urlopen("https://tieba.baidu.com/index.html")  #发出请求并且接收返回文本对象
html = response.read().decode('utf-8')   #调用read()进行读取，转换为utf-8的编码
# print(html)  #打印

# 注意，由于网页抓取下来的是bytes格式的数据，所以写入文件时需要以二进制的方式写入
fout = open('../data/txt.txt', 'wb')
html = html.encode()
fout.write(html)
fout.close()

fout = open('../data/html.html', 'wb')  # 写入到文件html.html
fout.write(html)
fout.close()