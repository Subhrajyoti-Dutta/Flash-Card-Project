import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
	DEBUG = False
	DB_DIR = None
	SQLALCHEMY_DATABASE_URI = None
	SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
	# DB_DIR = os.path.join(basedir, '../db_directory')
	SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, '../db_directory', 'testdb.sqlite3')
	DEBUG = True

class ProductionConfig(Config):
	DB_DIR = os.path.join(basedir, '../db_directory')
	SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(DB_DIR, 'proddb.sqlite3')
	DEBUG = False