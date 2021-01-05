import os

from flask import Flask, render_template, request, redirect, jsonify, make_response
from flask_dropzone import Dropzone


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'uploads'),
    DROPZONE_MAX_FILE_SIZE=1024,
    DROPZONE_TIMEOUT=5*60*1000,
    DROPZONE_ALLOWED_FILE_CUSTOM=True,  # 允许上传自定义文件格式
    DROPZONE_MAX_FILES=30,  # 一次最大上传文件数量
    DROPZONE_ALLOWED_FILE_TYPE='image/*, .pdf, .txt, .zip, .jar, .doc,'
                               '.docx, .xls, .xlsx ',)

dropzone = Dropzone(app)


@app.route('/',methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        if str(f.filename) == '屈永飞-4年-Python自动化测试.docx':
            return 'file is exits'
        f.save(os.path.join(app.config['UPLOADED_PATH'],f.filename))
    return render_template('index.html')


@app.route("/upload-video", methods=["GET", "POST"])
def upload_video():
    if request.method == "POST":

        filesize = request.cookies.get("filesize")
        file = request.files['file']

        print(f'Filesize: {filesize}')
        print(file)

        res = make_response(jsonify({"message": f"{file.filename} uploaded"}), 200)

        return res

    return render_template('upload_video.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
