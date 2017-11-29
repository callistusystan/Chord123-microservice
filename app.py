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
ALLOWED_EXTENSIONS = set(['txt', 'docx'])

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST'])
def translate():
    file = request.files['file']
    key = request.form['key']
    if not file or not allowed_file(file.filename) or not key:
        res = {}
        res["message"] = "Error: FILE and KEY must be provided"
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
    # base64.b64encode(f.getvalue()).decode()
    return base64.b64encode(f.getvalue()).decode()
    # return send_file(f, as_attachment=True, attachment_filename="out.docx")

    # chord123.translate('./data/You Are Here.docx', 'A', 'output.docx')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
