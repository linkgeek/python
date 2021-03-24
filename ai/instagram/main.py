# third-party imports
import os
from flask import Flask
from flask import request
from flask import render_template
from datetime import timedelta
from Gotham import gotham
from skimage import io, filters


def Run(path, pic_name, mode):
    functions = {'1': gotham}  # '0': cartoon, , '4':ink, '3':lomo, '2':sepia, '5':wald, '6':neg, '7':pop, '8':nash
    img = io.imread(path)  # 读取图片
    final = functions[mode](img)
    filename = './static/out/{}.jpg'.format(functions[mode].__name__)
    io.imsave(filename, final)
    return filename


app = Flask(__name__)
# Cancel image caching
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
ALLOWED_EXTENSIONS = set(['bmp', 'png', 'jpg', 'jpeg'])
UPLOAD_FOLDER = r'./static/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('template2.html')


@app.route('/url', methods=['GET', 'POST'])
def url():
    if request.method == 'POST':
        file = request.files['image']
        mode = request.form['mask']
        print(request.form['mask'])
        if file and allowed_file(file.filename):
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)
            output = Run(path, file.filename, mode)
            print(output)
            # output = add(path, file.filename, mode, isGoggle)
            return render_template('template2.html', output=output)
        else:
            return render_template('template2.html', alert='文件类型必须是图片！')
    else:
        return render_template('template2.html')


if __name__ == '__main__':
    app.run(debug=True)
