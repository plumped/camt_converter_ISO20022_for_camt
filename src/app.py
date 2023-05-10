from flask import Flask, flash, render_template, request, redirect, url_for, send_file
import os

from werkzeug.utils import secure_filename

import xmlparser

UPLOAD_FOLDER = "./uploads"
DOWNLOAD_FOLDER = "./archives"
ALLOWED_EXTENSIONS = {'zip'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.secret_key = "0ac1476b38841d44cee5e1d55d295c6c9625784634a50878e6c7c37cab10cae9"


@app.route('/')
def index():
    xmlparser.clear_parsed_files()
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/uploaded')
def uploaded():
    items = xmlparser.get_parsed_files()
    return render_template('uploaded.html', items=items)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Please select a *.zip file first!')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            xmlparser.clear_parsed_files()
            xmlparser.parse_xml_files()
            return redirect(url_for('uploaded'))
        else:
            flash('Wrong filetype! Please choose a *.zip file.')
            return redirect(request.url)


@app.route('/archives/<filename>', methods=['GET', 'POST'])
def download_file(filename):
    file_path = os.path.join(app.config["DOWNLOAD_FOLDER"], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return f"{filename} does not exist."


if __name__ == '__main__':
    app.run(host='0.0.0.0')
