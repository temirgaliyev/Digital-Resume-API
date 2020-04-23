from flask import Blueprint
from application import mongo

test = Blueprint('test', __name__)

@test.route("")
def home():
	# return str(mongo.db)
	from models import UserModel

	user = UserModel('John', 'Doe', 'john@doe.com', hash('original_password'), '+123456789')
	user = UserModel.insert(user)
	return str(user)

