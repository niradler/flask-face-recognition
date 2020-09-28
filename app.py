import flask
import os
import numpy as np
from flask import request, jsonify, redirect, render_template, abort
from recognition import face_recognition_helper
from functools import wraps
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")
STAGE = os.getenv("STAGE", "prod")

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if STAGE == "dev" or request.args.get('key') and request.args.get('key') == API_KEY:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
@require_appkey
def upload_file():
    uploaded_file = request.files['img']
    name = request.form.get('name')
    if uploaded_file.filename != '':
        uploaded_file.save(os.path.join("img", uploaded_file.filename))
    return redirect('/')


@app.route('/recognition', methods=['POST'])
@require_appkey
def recognition():
    uploaded_file = request.files['img']
    name = request.form.get('name')
    if uploaded_file.filename == '':
        return "<h1>400</h1><p>Missing Image file.</p>", 400
    if name == None:
        return "<h1>400</h1><p>Missing Name.</p>", 400
    file_path = os.path.join("img", uploaded_file.filename)
    uploaded_file.save(file_path)
    encoding = face_recognition_helper.recognize(file_path, name)

    return jsonify({
        "name": name,
        "encoding": list(encoding)
    })


@app.route('/compare', methods=['POST'])
@require_appkey
def compare():
    uploaded_file = request.files['img']
    if uploaded_file.filename == '':
        return "<h1>400</h1><p>Missing Image file.</p>", 400

    file_path = os.path.join("img", uploaded_file.filename)
    uploaded_file.save(file_path)
    name = face_recognition_helper.compare(file_path)

    return jsonify({
        "name": name
    })


@ app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>Not Found.</p>", 404


app.run()
