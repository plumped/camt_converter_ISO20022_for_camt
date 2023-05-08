import os
import xmlparser
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = "./uploads"
DOWNLOAD_FOLDER = "./archives"
ALLOWED_EXTENSIONS = {'zip'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.secret_key = "0ac1476b38841d44cee5e1d55d295c6c9625784634a50878e6c7c37cab10cae9"


@app.route('/')
def index():
    xmlparser.filelist.clear()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')

@app.route('/uploaded', methods=['GET', 'POST'])
def uploaded():
    items = xmlparser.filelist
    if request.method == 'POST':
        return redirect(url_for('download_file', name='csvperiban.zip'))
    return render_template('uploaded.html', items=items)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('Please select a *.zip file first!')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            xmlparser.xml_parsing()
            return redirect(url_for('uploaded'))
        else:
            flash('Wrong filetype! Please choose a *.zip file.')
            return redirect(request.url)
    return


@app.route('/archives/<name>')
def download_file(name):
    return send_from_directory(app.config["DOWNLOAD_FOLDER"], name)
