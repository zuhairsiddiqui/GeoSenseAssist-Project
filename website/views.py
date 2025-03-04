from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/') # will run for main page
def home():
  return render_template("website.html")