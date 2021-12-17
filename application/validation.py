from werkzeug.exceptions import HTTPException
from flask import make_response
import json

class NotFoundError(HTTPException):
	def __init__(self, status_code):
		self.response = make_response("", status_code)

class DeckError(HTTPException):

	deck_error_codes = {
		"DE1001" : "Deck not found",
		"DE1002" : "Deck name already exists"
	}

	def __init__(self, status_code, error_code):

		message = {
			"error_code" : error_code,
			"error_message" : DeckError.deck_error_codes[error_code]
		}

		self.response = make_response(json.dumps(message, indent = 4), status_code)

class UserError(HTTPException):

	user_error_codes = {
		"UE1001" : "User not found",
		"UE1002" : "User id already exists",
		"UE1003" : "User is an admin",
		"UE1004" : "Password and name cannot be blank",
		"UE1005" : "Password must be atleast 4 letters or more"
	}

	def __init__(self, status_code, error_code):

		message = {
			"error_code" : error_code,
			"error_message" : UserError.user_error_codes[error_code]
		}

		self.response = make_response(json.dumps(message, indent = 4), status_code)

class CardError(HTTPException):

	card_error_codes = {
		"CE1001" : "Card not found",
		"CE1002" : "Card already exists",
		"CE1003" : "card_word and card_ans cannot be blank"
	}

	def __init__(self, status_code, error_code):

		message = {
			"error_code" : error_code,
			"error_message" : CardError.card_error_codes[error_code]
		}

		self.response = make_response(json.dumps(message, indent = 4), status_code)
