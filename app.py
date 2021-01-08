import os
import time

from flask import Flask, render_template, request, redirect, jsonify, make_response
from flask_dropzone import Dropzone

from FileManageApp.util import format_size

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'uploads'),
    DROPZONE_MAX_FILE_SIZE=1024,
    DROPZONE_TIMEOUT=5*60*1000,
    DROPZONE_ALLOWED_FILE_CUSTOM=True,  # 允许上传自定义文件格式
    DROPZONE_MAX_FILES=30,  # 一次最大上传文件数量
    DROPZONE_ALLOWED_FILE_TYPE='image/*, .pdf, .txt, .zip, .jar, .doc,'
                               '.docx, .xls, .xlsx',)

dropzone = Dropzone(app)


@app.route('/',methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')

        f.save(os.path.join(app.config['UPLOADED_PATH'],f.filename))
    return render_template('basepage.html')


@app.route("/upload-file", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":

        filesize_byte = request.cookies.get("filesize")
        file = request.files['file']
        file_size = format_size(filesize_byte)
        FileType = 'video'
        file.save(os.path.join(app.config['UPLOADED_PATH'], file.filename))
        # 格式化成2021-03-20 11:45:39形式
        date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        res = make_response(jsonify(
            {
                "message": f"{file.filename} uploaded",
                "fize_msg": (file.filename, FileType, file_size, date_time)

             }), 200)
        return res

    return render_template('upload_file.html')

#
# @app.route("/download", methods=["GET", "POST"])
# def download_file():
#     pass


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
