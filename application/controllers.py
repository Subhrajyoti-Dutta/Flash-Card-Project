from flask import Flask, request
from flask import render_template
from flask import current_app as app
from application.models import *

db.create_all()

@app.route("/", methods=["GET"])
def index():
	return render_template('login.html')

