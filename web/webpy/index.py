#!/usr/bin/python
# -*- coding: UTF-8 -*-
import web
import os
import datetime

# 绝对路径
work_dir = os.path.dirname(os.path.abspath(__file__))
# 把当前路径切换到文件所在的路径
os.chdir(work_dir)

urls = (
    '/upload/\d+', 'upload',
    '/(.*)', 'hello'
)
app = web.application(urls, globals())


class hello:
    def GET(self, name):
        return open(r'./upload.html', 'r').read()


class upload:
    def POST(self):
        x = web.input(myfile={})
        filedir = '.'
        if 'myfile' in x:
            filename = x.myfile.filename
            # 将windows路径转为linux路径
            # filepath = x.myfile.filename.replace('\\', '/')

            # filename = filepath.split('/')[-1]  # the filename with extension
            # fout = open(filedir + '/' + filename, 'wb')
            # # str = x.myfile.file.read()
            # fout.write(x.myfile.value)
            # fout.close()

            with open(filedir + '/' + filename, 'wb', encoding="utf-8") as f_out:
                f_out.write(x.myfile.value)
                f_out.close()
        raise web.seeother('/')


class UploadFile:
    def POST(self):
        files = web.input(file_path={})
        if 'file_path' in files:
            homedir = os.getcwd()
            filedir = '%s/static/upload/img' % homedir
            filepath = files.file_path.replace('\\', '/')
            ext = filepath.split('.', 1)[1]
            file_name = '2021.' + ext
            print(homedir, files.file_path)
            exit()
            try:
                with open(files.file_path, 'rb', encoding="gbk") as f_in:
                    data = f_in.read()
                    f_in.close()
                    with open(filedir + '/' + file_name, 'wb', encoding="utf-8") as f_out:
                        f_out.write(data)
                        f_out.close()
            except:
                return 'faild'
            return '/static/upload/img/' + file_name


if __name__ == "__main__":
    app.run()
