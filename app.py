import os
from flask import Flask, flash, request, jsonify, render_template, send_file
from werkzeug.utils import secure_filename
import argparse
import numpy as np
from model import *

UPLOAD_FOLDER = './uploads'
OUTPUT_FOLDER = './output'
ALLOWED_EXTENSIONS = {'txt', 'out'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

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
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            ## clear cache if needed
            files = os.listdir(app.config['UPLOAD_FOLDER'])
            for f in files:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            ## clear output folder
            files = os.listdir(app.config['OUTPUT_FOLDER'])
            for f in files:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))

            ## Run the parsing
            FDS2Excel(os.path.join(app.config['UPLOAD_FOLDER'], filename), os.path.join(app.config['OUTPUT_FOLDER'], "output.xlsx"))

            # return ("UPLOADED:" + filename)
            return send_file(os.path.join(app.config['OUTPUT_FOLDER'], "output.xlsx"), attachment_filename='output.xlsx')

    return render_template('index.html')

if __name__ == "__main__":
    ## parse arguments for debug mode
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--debug", action="store_true", help="debug flask")
    args = vars(ap.parse_args())

    if args["debug"]:
        app.run(debug=True, port=8080)
    else:
        app.run(host='0.0.0.0', threaded=True ,port=8080)