import os
import subprocess


def getText():
    filepath = "D:/Code/python/spider/qinghua.txt"
    with open(filepath, 'r+', encoding='utf-8') as f:  # 打开文件
        content = f.read()  # 读取
        content = content.split("!@#$%")
        res = content[0]
        # del content[0]
        contentStr = '!@#$%'.join(content)
    with open(filepath, 'w', encoding='utf-8') as f2:  # 打开文件
        f2.write(contentStr)
        f.close()
        f2.close()
    return res


if __name__ == "__main__":
    str = getText()
    print(str)
    #os.system("open 'tencent://message/?uin=941192051&Site=&Service=201&sigT=2cf2671557dd'")
    os.system("open 'tencent://message/?Menu=yes&uin=941192051&Site=&Service=201&sigT=2cf2671557dd'")
    p1 = subprocess.Popen(["echo", str], stdout=subprocess.PIPE)
    subprocess.Popen(["pbcopy"], stdin=p1.stdout)
