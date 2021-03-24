'''
执行程序时要先彻底退出浏览器
'''

import browserhistory as bh
import pandas as pd
import csv


def get_browser_history() -> None:
    browser_history = bh.get_browserhistory()
    # 转换为表格
    # pd.DataFrame.from_dict(bh.get_browserhistory()['IE'])
    return browser_history


def write_browser_history_csv() -> None:
    browser_history = get_browser_history()
    for browser, history in browser_history.items():
        with open(browser + '_history.csv', mode='w', encoding='utf-8', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
            for data in history:
                csv.writer.writerow(data)


if __name__ == '__main__':
   write_browser_history_csv()