from application.database import db
import datetime

from flask import current_app as app

engine = db.create_engine(
	app.config.get('SQLALCHEMY_DATABASE_URI'),
	app.config.get('SQLALCHEMY_ENGINE_OPTIONS')
)

class Users(db.Model):
	__tablename__ = 'users'
	user_id = db.Column(db.String, primary_key = True, unique = True, nullable = False)
	user_pwd = db.Column(db.String, nullable = False)
	user_name = db.Column(db.String, nullable = False)
	permissions = db.Column(db.String, default = 'User', nullable = False)

class Decks(db.Model):
	__tablename__ = 'deck'
	deck_no = db.Column(db.Integer, primary_key=True,autoincrement=True)
	deck_name = db.Column(db.String, unique = True)
	number_of_cards = db.Column(db.Integer, default = 1)
	creator = db.Column(db.String, default = 'Admin')
	creation_date = db.Column(db.Date)

class Record(db.Model):
	__tablename__ = 'record'
	user_id = db.Column(db.String, db.ForeignKey('users.user_id'), primary_key=True)
	deck_no = db.Column(db.String, db.ForeignKey('deck.deck_no'), primary_key=True)
	last_review = db.Column(db.Date)

class UserData(db.Model):
	__tablename__ = 'userdata'
	user_id = db.Column(db.String, db.ForeignKey('users.user_id'), primary_key=True)
	deck_no = db.Column(db.String, db.ForeignKey('deck.deck_no'), primary_key=True)
	card_no = db.Column(db.Integer, primary_key=True)
	diff = db.Column(db.Integer)

def newDeckMaker(deckName):
	class Deck(db.Model):
		__tablename__ = deckName
		card_no = db.Column(db.Integer,autoincrement=True)
		card_word = db.Column(db.String,primary_key=True)
		card_ans = db.Column(db.String)
	db.create_all()
	return Deck

class DeckList:
	decks = {deck.deck_name : newDeckMaker(deck.deck_name) for deck in Decks.query.all()}

	def get(deck_name):
		return DeckList.decks[deck_name]

	def post(deck_name):
		DeckList.decks[deck_name] = newDeckMaker(deck_name)

	def delete(deck_name):
		db.metadata.remove(DeckList.decks[deck_name].__table__)
		DeckList.decks[deck_name].__table__.drop(engine)
		del DeckList.decks[deck_name]

if __name__ == "__main__":
	new_deck = Decks(deck_name = "Synonyms", creation_date = datetime.date.today())
	db.session.add(new_deck)
	db.session.commit()
	# pass