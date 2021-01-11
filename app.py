import os
import time

from flask import Flask, render_template, request, redirect, jsonify, make_response, url_for
from flask_dropzone import Dropzone
import logging

from loguru import logger

from FileManageApp.model import database, query, query_name, update
from FileManageApp.util import format_size

basedir = os.path.abspath(os.path.dirname(__file__))
logger.add('flask.log')
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


@app.route('/')
def index():
    data = query()
    return render_template('upload_file.html', emp=data)


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":

        filesize_byte = request.cookies.get("filesize")
        file = request.files['file']
        file_size = format_size(filesize_byte)
        FileType = 'video'
        file.save(os.path.join(app.config['UPLOADED_PATH'], file.filename))
        # 格式化成2021-03-20 11:45:39形式
        date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        is_exit = query_name(str(file.filename))
        if is_exit == None:database(file.filename, FileType, file_size, date_time)
        else:update(date_time, str(file.filename))

        res = make_response(jsonify(
            {
                "message": f"{file.filename} uploaded",
                "file_msg": (file.filename, FileType, file_size, date_time),
             }), 200)
        return res

    return render_template('upload_file.html')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
