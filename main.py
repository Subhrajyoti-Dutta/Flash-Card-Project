from flask import Flask
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db

def createApp():
	flaskApp = Flask(__name__, template_folder = "templates")
	flaskApp.config.from_object(LocalDevelopmentConfig)
	db.init_app(flaskApp)
	flaskApp.app_context().push()
	return flaskApp

app = createApp()

from application.controllers import *

if __name__ == "__main__":
	app.run(
		host = '127.0.0.1',
		port = '8080'
	)