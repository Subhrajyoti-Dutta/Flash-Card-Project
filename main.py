from flask import Flask
from flask_restful import Api
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db

def createApp():
	flaskApp = Flask(__name__, template_folder = "templates")
	flaskApp.config.from_object(LocalDevelopmentConfig)
	db.init_app(flaskApp)
	api = Api(flaskApp)
	flaskApp.app_context().push()
	return flaskApp, api

app, api = createApp()

from application.controllers import *

from application.api import *

api.add_resource(DeckListAPI, "/api/deck")
api.add_resource(DeckAPI,     "/api/deck/<string:deck_name>")
api.add_resource(CardAPI,     "/api/deck/<string:deck_name>/card/<int:card_no>")
api.add_resource(UserListAPI, "/api/user")
api.add_resource(UserAPI,     "/api/user/<string:user_id>")
api.add_resource(RecordAPI,   "/api/user/<string:user_id>/deck/<string:deck_name>")
api.add_resource(UserDataAPI, "/api/user/<string:user_id>/deck/<string:deck_name>/card/<int:card_no>")


if __name__ == "__main__":
	app.run(
		host = '127.0.0.1',
		port = '8080'
	)