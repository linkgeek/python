import requests
import re


def fuckLoveWords():
    with open("../data/config/qinghua.txt", "w", encoding="utf-8") as f:
        for i in range(1000, 1200):
            print("第" + str(i) + "页")
            try:
                url = "http://www.ainicr.cn/qh/" + str(i) + ".html"
                response = requests.get(url).text
                counts = re.findall('<p>(.*?)</p></a>', response)
                for count in counts:
                    f.write(count + '!@#$%')
            except:
                pass


if __name__ == "__main__":
    fuckLoveWords()
