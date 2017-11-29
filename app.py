import base64
import json
from flask import Flask, request, redirect, url_for, send_file
from flask_cors import CORS, cross_origin
from chord123 import chord123
from werkzeug import secure_filename
import io
import os

UPLOAD_FOLDER = './tmp/'
OUTPUT_FOLDER = './out/'
ALLOWED_EXTENSIONS = set(['docx'])

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    return "Hey, how did you get here!? Anyway, nothing to see here!"

@app.route('/translate', methods=['POST'])
def translate():
    file = request.files['file']
    key = request.form['key']
    if not file or not allowed_file(file.filename) or not key:
        res = {}
        res["message"] = "Error: file and key must be provided!"
        return json.dumps(res)
    filename = secure_filename(file.filename)
    inputpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    file.save(inputpath)
    outputpath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    f = io.BytesIO()
    chord123.translate(inputpath, key, f)
    f.seek(0)
    return base64.b64encode(f.getvalue()).decode()

@app.route('/transpose', methods=['POST'])
def transpose():
    file = request.files['file']
    origKey = request.form['origKey']
    targetKey = request.form['targetKey']
    if not file or not allowed_file(file.filename) or not origKey or not targetKey:
        res = {}
        res["message"] = "Error: file, origKey and targetKey must be provided!"
        return json.dumps(res)
    filename = secure_filename(file.filename)
    inputpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    file.save(inputpath)
    outputpath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    f = io.BytesIO()
    chord123.transpose(inputpath, origKey, targetKey, f)
    f.seek(0)
    return base64.b64encode(f.getvalue()).decode()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
