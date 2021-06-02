# 文件上传
import flask, os, sys, time
from flask import request

interface_path = os.path.dirname(__file__)
sys.path.insert(0, interface_path)  # 将当前文件的父目录加入临时系统变量

server = flask.Flask(__name__, static_folder='static')


@server.route('/', methods=['get'])
def index():
    return '<form action="/upload" method="post" enctype="multipart/form-data"><input type="file" id="img" name="img"><button type="submit">上传</button></form>'


@server.route('/upload', methods=['post'])
def upload():
    fname = request.files['img']  # 获取上传的文件
    if fname:
        t = time.strftime('%Y%m%d%H%M%S')
        new_fname = r'static/' + t + fname.filename
        fname.save(new_fname)  # 保存文件到指定路径
        return '<img src=%s>' % new_fname
    else:
        return '{"msg": "请上传文件！"}'


print('----------路由和视图函数的对应关系----------')
print(server.url_map)  # 打印路由和视图函数的对应关系
server.run(port=8000)
