from flask import Blueprint
from flask_restful import Resource, Api
from application import mongo

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

# @api_blueprint.route("")
# def home():
# 	# return str(mongo.db)
# 	from models import UserModel

# 	user = UserModel('John', 'Doe', 'john@doe.com', hash('original_password'), '+123456789')
# 	user = UserModel.insert(user)
# 	return str(user)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')
