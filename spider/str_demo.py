import re

# 模糊匹配List
def fuzzyMatch():
    value = '西西'
    list = ['大海西西的', '大家西西', '打架', '西都好快', '西西大化']
    tempList = []
    pattern = '.*' + value + '.*'
    for s in list:
        obj = re.findall(pattern, s)
        if len(obj) > 0:
            tempList.extend(obj)
    print(tempList)  # 输出: ['大海西西的', '大家西西', '西西大化']




def main():

    keywords = 'YMDD'
    pattern = '.*' + keywords + '.*'


    str1 = 'ssymdd-这是'
    print(str1.find(keywords))

    str2 = 'ssYMDD-这是2'
    print(str2.find(keywords))

    obj = re.findall(pattern, str2)
    if len(obj) > 0:
        print(': 符合')

if __name__ == '__main__':
    # main()
     fuzzyMatch()