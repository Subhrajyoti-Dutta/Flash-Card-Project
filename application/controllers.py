from flask import Flask, request
from flask import render_template
from flask import current_app as app
from application.models import *

@app.route("/", methods=["GET"])
def index():
	return render_template('login.html')