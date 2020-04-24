from flask import Blueprint
from application import mongo

test_blueprint = Blueprint('test', __name__)

@test_blueprint.route("")
def home():
	# return str(mongo.db)
	from models import UserModel

	user = UserModel('Arystan', 'Amanzholov', 'arysisthebest@2k.20', hash('arysisthebest'), '+77bestphone')

	user = UserModel.insert_from_model(user)
	return str(user)

