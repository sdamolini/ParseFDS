import numpy as np
from flask import Flask, request, jsonify, render_template
import argparse
from werkzeug.utils import secure_filename


# create flask app
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
MAX_CONTENT_LENGTH = 500*1000*1000

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# home page
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'

if __name__ == "__main__":
    ## parse arguments for debug mode
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--debug", action="store_true", help="debug flask")
    args = vars(ap.parse_args())

    if args["debug"]:
        app.run(debug=True, port=8080)
    else:
        app.run(host='0.0.0.0', threaded=True ,port=8080)