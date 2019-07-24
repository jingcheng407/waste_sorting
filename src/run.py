from flask import Flask, request
from werkzeug import secure_filename
import timeit
import os

import test

category = ['废纸板、纸板箱', '废玻璃、玻璃瓶', '废金属罐', '废报纸、废杂志', '废塑料盒、塑料瓶']

app = Flask(__name__)


def save_pic(f):
    file_name = str(timeit.default_timer()) + secure_filename(f.filename)
    file_path = os.path.join(os.path.dirname(__file__), '..', 'upload_pic', file_name)
    f.save(file_path)


@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    save_pic(f)
    a, b = test.f(f)
    conf = a.max()
    if conf < 0.6:
        return '垃圾类别是:' + category[b] + ' || 置信度为:' + str(a.max()) + ' || 置信度过低, 建议返回人工检测'
    else:
        return '垃圾类别是:' + category[b] + ' || 置信度为:' + str(a.max())


@app.route('/')
def index():
    return '''
    <!doctype html>
    <html>
    <body>
    <form action='/upload' method='post' enctype='multipart/form-data'>
        <input type='file' name='file'>
    <input type='submit' value='Upload'>
    </form>
    '''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
