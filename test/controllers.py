from flask import Blueprint
from application import mongo

test = Blueprint('test', __name__)

@test.route("")
def home():
	# return str(mongo.db)
	from data.models import User

	user = User('John', 'Doe', 'john@doe.com', hash('original_password'), '+123456789')
	user = User.insert(user)
	return str(user)

