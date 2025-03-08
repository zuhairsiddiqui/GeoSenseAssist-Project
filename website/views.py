from flask import Flask, Blueprint, render_template, request, redirect
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
# built-in python library installed when you install python. it helps make sure files uploaded are safe.
import os
# https://www.youtube.com/watch?v=GQLRVhXnZkE

app = Flask(__name__)
app.config['UPLOAD_DIRECTORY'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB

views = Blueprint('views', __name__)

@views.route('/') # will run for main page
def home():
  return render_template("website.html")

@views.route('/login')
def login():
  return render_template("login.html")

@views.route('/logout')
def logout():
  return render_template("logout.html")

@views.route('/sign-up')
def signup():
    return render_template("signup.html")

@views.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['fileUpload']

        if file:
            file.save(os.path.join(app.config['UPLOAD_DIRECTORY'], secure_filename(file.filename)))
            
    except RequestEntityTooLarge:
        return "File is larger than the 16 MB Limit"

    return redirect('/')
