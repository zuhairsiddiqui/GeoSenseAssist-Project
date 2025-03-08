from flask import Blueprint, render_template

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

@views.route('sign-up')
def signup():
    return render_template("signup.html")