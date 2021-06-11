import os
import requests


class IFund:
    def get_realtime_rise(self, code):
        try:
            url = "http://gz-fund.10jqka.com.cn/?module=api&controller=index&action=chart&info=vm_fd_" + row[-5:][
                1] + "&start=" + time + "&"
            # 改变爬虫头
            headers = {
                "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
            data = requests.get(url)
            data.encoding = "UTF-8"
            datasplit = data.text.split("|")
            datasplit1 = datasplit[1].split(";")
            datasplit2 = datasplit[1].split(",")
            # print(datasplit2)
            mx = float(datasplit2[1]) - float(datasplit2[2])
            rata = mx / float(datasplit2[2]) * 100
        except:
            print(row, "error")