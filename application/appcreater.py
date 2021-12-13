from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db

def createApp():
	flaskApp = Flask(__name__, template_folder = "../templates")
	flaskApp.config.from_object(LocalDevelopmentConfig)
	db.init_app(flaskApp)
	flaskApp.app_context().push()
	return flaskApp