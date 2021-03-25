import requests
from lxml import etree

text = '''
<div>
    <ul class="list">
        <li>
            <a href="https://s1.bdstatic.com/"><b>item 1</b></a>
        </li>
        <li>
            "[03-25] "
            <a href="https://s2.bdstatic.com/">
                <script></script>
                "title 2"
                <font>1024</font>
            </a>
        </li>
        <li>
            "[03-24] "
            <a href="https://s3.bdstatic.com/">
                <script></script>
                "title 3"
                <font>1024</font>
            </a>
        </li>
    </ul>     
</div>
'''

# 利用 etree.HTML 把字符串解析成 HTML 文件
html = etree.HTML(text)
# decode() 方法将其转化为 str 类型
s = etree.tostring(html).decode()
print(s)
exit(234)

# 此时responses是一个list[]
response = html.xpath('//textarea [@id="hotsearch_data"]/text()')
print(response)
exit(234)

# 此时遍历response得到item(item为字典类型)
for item in response:
    # 通过key获取item的value----item2
    item2 = eval(item).get("hotsearch")  # 此处需要用eval智能识别item的类型
    # item2也是一个list,再次遍历得到item3
    for item3 in item2:
        # item3也是字典类型，通过key('pure_title')得到value
        print(item3.get('pure_title'))