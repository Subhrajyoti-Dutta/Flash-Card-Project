from flask import current_app as app

from flask_restful import Resource
from flask_restful import reqparse

from application.database import db
from application.models import *
from application.validation import *

import requests
import datetime


class DeckListAPI(Resource):
	def get(self):
		decks = Decks.query.all()
		return {
			"number_of_decks" : len(decks),
			"list_of_decks" : [
				{
					"deck_no" : deck.deck_no,
					"deck_name" : deck.deck_name,
					"creator" : deck.creator
				}
				for deck in decks
			]
		}, 200

	def post(self):

		request = reqparse.RequestParser()
		request.add_argument("deck_name")

		args = request.parse_args()

		deck_name = args.get(deck_name)

		if Decks.query.filter_by(deck_name = deck_name).first():
			raise DeckError(
				status_code = 401,
				error_code = "DE1002",
			)

		#creating deck table
		DeckList.post(deck_name)

		#adding deck name to deck list
		new_deck = Decks(
			deck_name = deck_name,
			number_of_cards = 0,
			creation_date = datetime.date.today()
		)

		db.session.add(new_deck)
		db.session.commit()

		return {
			"task" : "Successful",
			"new_deck_name" : deck_name
		}, 200

class DeckAPI(Resource):
	def get(self, deck_name):
		deck = Decks.query.filter_by(deck_name = deck_name).first()
		
		if deck is None:
			raise DeckError(
				status_code = 404,
				error_code = "DE1001"
			)

		cards = DeckList.get(deck_name).query.all()

		return {
			"Deck No" : deck.deck_no,
			"Deck Name" : deck.deck_name,
			"Creator" : deck.creator,
			"Date of Creation" : deck.creation_date.strftime("%Y-%m-%d"),
			"Number of Cards" : deck.number_of_cards,
			"List of Cards" : [
				{
					"card_no" : card.card_no,
					"card_word" : card.card_word,
					"card_ans" : card.card_ans
				}
				for card in cards
			]
		}, 200

	def delete(self, deck_name):
		delete_deck = Decks.query.filter_by(deck_name = deck_name).first()

		if delete_deck is None:
			raise DeckError(
				status_code = 404,
				error_code = "DE1001"
			)

		db.session.delete(delete_deck)
		db.session.commit()

		DeckList.delete(deck_name)

		return {
			"task" : "Successful",
			"deleted_deck_name" : deck_name
		}, 200

	def post(self, deck_name):
		request = reqparse.RequestParser()
		request.add_argument("card_word")
		request.add_argument("card_ans")

		args = request.parse_args()

		card_word = args.get("card_word")
		card_ans = args.get("card_ans")

		if card_word is None or card_ans is None:
			raise CardError(
				status_code = 404,
				error_code = "CE1003"
			)

		deck = DeckList.get(deck_name)
		card = deck.query.filter_by(card_no=card_no).first()

		if card is not None:
			raise CardError(
				status_code = 404,
				error_code = "CE1002"
			)

		deck(
			card_word = card_word,
			card_ans = card_ans
		)

		db.session.commit()

		return {
			"task" : "Successful",
			"deck_name" : deck_name,
			"card_word" : card_word,
			"card_ans" : card_ans
		}, 200

class CardAPI(Resource):
	def get(self, deck_name, card_no):
		deck = DeckList.get(deck_name)
		card = deck.query.filter_by(card_no=card_no).first()

		if card is None:
			raise CardError(
				status_code = 404,
				error_code = "CE1001"
			)

		return {
			"card_no": card.card_no,
			"card_word" : card.card_word,
			"card_ans" : card.card_ans
		}, 200

	def put(self, deck_name, card_no):
		request = reqparse.RequestParser()
		request.add_argument("card_word")
		request.add_argument("card_ans")

		args = request.parse_args()

		deck = DeckList.get(deck_name)
		card = deck.query.filter_by(card_no=card_no).first()

		if card is None:
			raise CardError(
				status_code = 404,
				error_code = "CE1001"
			)

		card_word = args.get("card_word") if args.get("card_word") is not None else card.card_word
		card_ans = args.get("card_ans")	if args.get("card_ans") is not None else card.card_ans

		card.card_word = card_word
		card.card_ans = card_ans

		db.session.commit()

		return {
			"task" : "Successful",
			"deck_name" : deck_name,
			"card_no" : card_no,
			"card_word" : card_word,
			"card_ans" : card_ans
		}, 200

	def delete(self, deck_name, card_no):
		deck = DeckList.get(deck_name)
		delete_card = deck.query.filter_by(card_no=card_no).first()

		if delete_card is None:
			raise CardError(
				status_code = 404,
				error_code = "CE1001"
			)

		db.session.delete(delete_card)
		db.session.commit()

		return {
			"task" : "Successful",
			"deck_name" : deck_name,
			"deleted_card_no" : card_no,
			"deleted_card_word" : delete_card.card_word,
			"deleted_card_ans" : delete_card.card_ans
		}, 200

class UserListAPI(Resource):
	def get(self):
		# help(app)

		users = Users.query.all()
		return {
			"number_of_users" : len(users),
			"list_of_users" : [
				{
					"user_id" : user.user_id,
					"user_name" : user.user_name,
					"permissions" : user.permissions
				}
				for user in users
			]
		}, 200

class UserAPI(Resource):
	def get(self, user_id):
		user = Users.query.filter_by(user_id = user_id).first()

		if user is None:
			raise UserError(
				status_code = 404,
				error_code = "UE1001",
			)

		return {
			"user_id" : user.user_id,
			"user_name" : user.user_name
		}, 200

	def delete(self, user_id):
		delete_user = Users.query.filter_by(user_id=user_id).first()
		
		if delete_user is None:
			raise UserError(
				status_code = 404,
				error_code = "UE1001"
			)

		Record.query.filter_by(user_id=user_id).delete()

		db.session.delete(delete_user)
		db.session.commit()

		return {
			"task" : "Successful",
			"deleted_user_id" : user_id,
			"deleted_user_name" : delete_user.user_name
		}, 200

	def put(self, user_id):
		request = reqparse.RequestParser()
		request.add_argument("password")
		request.add_argument("name")

		args = request.parse_args()

		update_user = Users.query.filter_by(user_id = user_id).first()

		if update_user is None:
			raise UserError(
				status_code = 404,
				error_code = "UE1001",
			)

		user_name = args.get("name") if args.get("name") is not None else update_user.user_name
		user_pwd = args.get("password") if args.get("password") is not None else update_user.user_pwd

		update_user.user_name = user_name
		update_user.user_pwd  = user_pwd

		db.session.commit()

		return {
			"task" : "Successful",
			"user_id" : user_id,
			"user_name" : user_name,
			"user_password" : user_pwd[:2] + (len(user_pwd) - 2) * "*"
		}, 200

	def post(self, user_id):
		request = reqparse.RequestParser()
		request.add_argument("password")
		request.add_argument("name")

		args = request.parse_args()

		if Users.query.filter_by(user_id = user_id).first():
			raise UserError(
				status_code = 404,
				error_code = "UE1002",
			)

		user_name = args.get("name")
		password = args.get("password")

		if user_name is None or password is None:
			raise UserError(
				status_code = 400,
				error_code = "UE1004",
			)

		if len(password) < 4:
			raise UserError(
				status_code = 400,
				error_code = "UE1005",
			)

		new_user = Users(
			user_id   = user_id,
			user_name = user_name,
			user_pwd  = password
		)


		db.session.add(new_user)
		db.session.commit()

		return {
			"task" : "Successful",
			"new_user_id" : user_id,
			"new_user_name" : user_name,
			"new_user_password" : password[:2] + (len(password) - 2) * "*"
		}, 200

class RecordAPI(Resource):
	def get(self, user_id, deck_name):
		pass
	def delete(self, user_id, deck_name):
		pass
	def put(self, user_id, deck_name):
		pass
	def post(self, user_id, deck_name):
		pass

class UserDataAPI(Resource):
	def get(self, user_id, deck_name, card_no):
		pass
	def delete(self, user_id, deck_name, card_no):
		pass
	def put(self, user_id, deck_name, card_no):
		pass
	def post(self, user_id, deck_name, card_no):
		pass
