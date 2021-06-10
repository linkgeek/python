import os
from flask import Flask
from flask import request
from flask import render_template
from datetime import timedelta
from main import Beauty
import time

app = Flask(__name__)
# # 设置静态文件缓存过期时间
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
ALLOWED_EXTENSIONS = set(['bmp', 'png', 'jpg', 'jpeg'])
UPLOAD_FOLDER = r'./static/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/beauty', methods=['GET', 'POST'])
def beauty():
    if request.method == 'POST':
        file = request.files['image']
        print(file)
        if file and allowed_file(file.filename):
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)
            output = Beauty(path, file.filename)
            print(output)
            return render_template('index.html', output=output)
        else:
            return render_template('index.html', alert='文件类型必须是图片！')
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
