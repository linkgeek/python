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
        with open(browser + '_history.csv', mode='�GFn�J^�N�ډ����MD=]=F��gݴ���\�T�;�O���C
�s�9�}4FI����3+<39ȏ�<�Ȧ0�
O��=ԟ3��l� ���B��2F�h%�X����ه��������4����/�M�ƣ"SJ�IL�f�/yc��P7���?;�d׾9����;c�Sye돜�V݆S�� >5�<�
��]���a23R���"�!��gMT<�qIӆ+	\/)��R�T�8;B��}���ɡc>�I~����%q