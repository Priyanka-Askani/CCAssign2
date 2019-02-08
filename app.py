from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask import jsonify

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

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
	upvotes = db.Column(db.Integer, nullable = False, default = 0)
	image = db.Column(db.String(100),nullable = False, default = "default.jpg")
	cat_name = db.Column(db.String(20),db.ForeignKey('category.id'))
	username = db.Column(db.String(20),db.ForeignKey('user.username'))
	timestamp = db.Column(db.DateTime, default = datetime.utcnow)

	def __repr__(self):
		return "Act id is {}".format(self.act_id)

@app.route('/api/v1/categories/<categoryname>/acts/size', methods = ['GET'])
def get_number_of_acts(categoryname):
	if request.method == 'GET':
		# first check if categoryname is present or not
		category = Category.query.filter_by(cat_name=categoryname).all()
		if len(category) == 0:
			return jsonify(name='bhar'),204

		acts = Act.query.filter_by(cat_name=categoryname).all()
		size = len(acts)
		if size == 0:
			return jsonify(name='here'),204

		return jsonify(size=size)

@app.route('/api/v1/acts/upvote',methods = ['POST'])
def upvote_request():
	if request.method == 'POST':
		if act_id in request.form.keys():
			act_id = request.form['act_id']

			act_obj = Act.query.filter_by(act_id=act_id).all()

			if len(act_obj) == 0:
				return jsonify({}),404

			act_obj[0].upvotes += 1 # only 1 obj should exist

			db.session.commit()

			return jsonify({}),200

		else:
			return jsonify({}),400

@app.route('/api/v1/acts/<actid>',methods = ['DELETE'])
def delete_act(actid):
	if request.method == 'DELETE':
		# check if act_id is present

		act = Act.query.filter_by(act_id=actid).all()

		if len(act) == 0:
			return jsonify({}),404

		db.session.delete(act[0]) # only 1 should exist

		db.session.commit()

		return jsonify({}),200

@app.route('/api/v1/acts',methods = ['POST'])
def upload_act():
	try:
		act_id = request.form['act_id']
		username = request.form['username']
		caption = request.form['caption']
		cat_name = request.form['cat_name']
		#imgB64 = request.form['imgB64']
	except KeyError:
		return jsonify({}),404

	if 'upvotes' in request.form.keys():
		return jsonify({}),404

	if 'imgB64' in request.form.keys():
		imgB64 = request.form['imgB64']
	else:
		imgB64 = 'default.jpg'

	# check if act_id already exists
	acts = Act.query.filter_by(act_id=int(act_id)).all()
	if len(acts) != 0:
		return jsonify({}),404

	# check if username exists
	user = User.query.filter_by(username=username).all()
	if len(user) == 0:
		return jsonify({}),404

	# check if category exists
	category = Category.query.filter_by(cat_name=cat_name).all()
	if len(category) == 0:
		return jsonify({}),404

	act = Act(act_id=act_id,username=username,caption=caption,cat_name=cat_name,image = imgB64)

	db.session.add(act)

	db.session.commit()

	return jsonify({}),200

@app.route('/api/v1/categories/<categoryname>/acts',methods=['GET'])
def return_no_in_range(categoryname):
	start = request.args.get('start','')
	end = request.args.get('end','')

	return jsonify(start=start,end=end),200