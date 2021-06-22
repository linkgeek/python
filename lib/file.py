#!/usr/bin/env python
# encoding: utf-8
import os
import time
import pdfkit
from urllib.request import urlopen
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams


class FileUtil:

    @staticmethod
    def read_txt(path):
        """
        读取文件文本
        path 文件路径
        """
        f = open(path, encoding="utf-8")
        data = f.read()
        f.close()
        return data

    @staticmethod
    def read_pdf():
        # 获取文档
        # fp = open("naacl06-shinyama.pdf", 'rb')
        pdf_url = 'http://file.finance.sina.com.cn/211.154.219.97:9494/MRGG/CNSESH_STOCK/2021/2021-5/2021-05-12/7239797.PDF'
        fp = urlopen(pdf_url)

        # 创建解释器
        parser = PDFParser(fp)

        # PDF文档对象
        doc = PDFDocument()

        # 连接解释器和文档对象
        parser.set_document(doc)
        doc.set_parser(parser)

        # 初始化文档
        doc.initialize()

        # 创建PDF资源管理器
        resource = PDFResourceManager()

        # 创建一个PDF参数分析器
        laparam = LAParams()

        # 创建聚合器
        device = PDFPageAggregator(resource, laparams=laparam)

        # 创建PDF页面解析器
        interpreter = PDFPageInterpreter(resource, device)

        # 循环遍历列表，每次处理一页的内容
        # doc.get_pages() 获取page列表
        for page in doc.get_pages():
            # 使用页面解释器来读取
            interpreter.process_page(page)
            # 使用聚合器获得内容
            layout = device.get_result()
            for out in layout:
                if isinstance(out, LTTextBoxHorizontal):
                    print(out.get_text())
                # if hasattr(out, 'get_text'):
                #     print(out.get_text())

    @staticmethod
    def get_ban_copy_page():
        """
        获取禁止复制网页 生成pdf
        安装 wkhtmltopdf https://wkhtmltopdf.org/downloads.html
        """
        url = "https://www.jianshu.com/p/717dc02a9c21"
        config = pdfkit.configuration(wkhtmltopdf=r'D:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        pdfkit.from_url(url, r"G:\Code\python\data\txt\%s.pdf"
                        % time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())), configuration=config)


# if __name__ == '__main__':
#     til = FileUtil()
#     util.get_ban_copy_page()
