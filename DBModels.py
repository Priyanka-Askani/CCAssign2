from __main__ import db
from datetime import datetime

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20), unique = True, nullable = False)
	password = db.Column(db.String(256), nullable = False) 
	acts = db.relationship('Act', backref = "user", lazy = True)

	def __repr__(self):
		return "User is {}".format(self.username)

class Category(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	cat_name = db.Column(db.String(20), unique = True, nullable = False)

	def __repr__(self):
		return "Category name is {}".format(self.cat_name)

class Act(db.Model):
	act_id = db.Column(db.Integer, primary_key = True)
	caption = db.Column(db.String(100), nullable = False)
	upvotes = db.Column(db.Integer, nullable = False)
	image = db.Column(db.String(100),nullable = False, default = "default.jpg")
	cat_name = db.Column(db.String(20),db.ForeignKey('category.id'))
	username = db.Column(db.String(20),db.ForeignKey('user.username'))
	timestamp = db.Column(db.DateTime, default = datetime.datetime.utcnow)

	def __repr__(self):
		return "Act id is {}".format(act_id)