# 打开浏览器

import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import webbrowser as wb


# system方法
def system():
    os.system('"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" http://www.baidu.com')
    # 打开新窗口
    # os.startfile(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")


# 无效
def mac():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get("http://huazhu.gag.com/mis/main.do")


# 无效
def selenium():
    url = 'http://www.baidu.com'
    driver = webdriver.Chrome()
    driver.get(url)


# webbrowser 方法
def web_browser(url=''):
    url = 'http://www.baidu.com'
    url2 = "https://pypi.org/project/selenium/"
    # wb.open("http://www.baidu.com")
    # new=0：同一浏览器窗口打开 1：打开浏览器新的窗口，2：打开浏览器窗口新的tab
    # autoraise=True:窗口自动增长
    # wb.open(url, new=0, autoraise=False)
    wb.open("https://www.jianshu.com/p/25a5c7454d30", new=1, autoraise=True)

    # wb.open("https://fanyi.baidu.com/?aldtype=16047#auto/zh", new=0)
    # os.startfile(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
    # wb.open("https://www.json.cn/", new=0)

    # wb.open_new(url)
    # wb.open_new_tab(url)


# 可行
def new_wb():
    chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
    chrome_path_NW = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s --new-window"
    strURL = "https://element.eleme.cn/#/zh-CN"

    controller = wb.get(chrome_path)
    controllerNW = wb.get(chrome_path_NW)

    controller.open(strURL, new=1)
    controller.open(strURL, new=2)
    controller.open("https://www.json.cn/", new=2)
    controllerNW.open(strURL, new=0)


def auto_open():

    url2 = 'https://seofangfa.com/proxy/'
    url_list = [1, 2, 3, 4, 5]
    m = 0
    for url in url_list:
        chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
        crl = wb.get(chrome_path)
        if m > 2:
            m = 0
            chrome_path_NW = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s --new-window"
            crl = wb.get(chrome_path_NW)
        crl.open(url2, new=0)
        print('url:{}, m:{}'.format(url, m))
        m += 1


def moni():
    # v = virtkey.virtkey()
    # v.press_keysym(65507)  # Ctrl键位
    # v.press_unicode(ord('v'))  # 模拟字母V
    # v.release_unicode(ord('v'))
    # v.release_keysym(65507)
    # time.sleep(5)
    # v.press_keysym(65421)  # Enter
    # v.release_keysym(65421)

    wb.open('https://pypi.org/search/?q=virtkey', new=0, autoraise=False)
    driver = webdriver.Chrome()
    driver.find_element_by_id("kw").send_keys(Keys.CONTROL, 'n')


def main():
    # mac()
    # selenium()
    # system()
    # web_browser()
    # new_wb()
    auto_open()
    # moni()


if __name__ == '__main__':
    main()
