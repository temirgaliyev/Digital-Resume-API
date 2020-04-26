# "{\"first_name\":\"name\", \"last_name\":\"surname\", \"email\":\"mail\", \"phone\":\"phone\", \"password\":\"password\"}"
# https://github.com/MongoEngine/mongoengine/blob/master/mongoengine/errors.py

from flask_restful import Resource
from flask import request
from mongoengine.errors import NotUniqueError, ValidationError, DoesNotExist

from models import User
from api.utils import custom_hash, abort_if_invalid_request_params


class UserApi(Resource):

	def get(self):
		args = request.args
		abort_if_invalid_request_params(args, ['email'])

		try:
			user_dict = User.objects.get(email=args['email']).to_mongo().to_dict()
			del user_dict['_id']
			return user_dict, 200

		except DoesNotExist as e:
			return {"type":"DoesNotExist","err": str(e)}, 400

		except Exception as e:
			return {"type":"Exception","err": str(e)}, 400


	def post(self):
		json = request.json
		abort_if_invalid_request_params(json, ['first_name', 'last_name', 'email', 'phone', 'password'])

		try:
			user = User()
			user.first_name = json['first_name']
			user.last_name = json['last_name']
			user.email = json['email']
			user.phone = json['phone']
			user.password = custom_hash(json['password'])
					
			user.save()
			user_dict = user.to_mongo().to_dict()
			del user_dict['_id']
			return user_dict, 200

		except NotUniqueError as e:
			return {"type":"NotUniqueError","err":str(e)}, 400

		except ValidationError as e:
			return {"type":"ValidationError", 'err':e.to_dict()}, 400

		except Exception as e:
			return {"type":"Exception","err": str(e)}, 400


	def put(self):
		json = request.json
		abort_if_invalid_request_params(json, ['email'])

		try:
			user = User.objects.get(email=json['email'])

		except DoesNotExist as e:
			return {"type":"DoesNotExist","err": str(e)}, 400

		except Exception as e:
			return {"type":"Exception","err": str(e)}, 400

		try:
			if 'first_name' in json and json['first_name'] != user['first_name']:
				user.update(first_name = json['first_name'])

			if 'last_name' in json and json['last_name'] != user['last_name']:
				user.update(last_name = json['last_name'])

			# if json['email']:
			# 	user.update(email = json['email'])

			if 'phone' in json and json['phone'] != user['phone']:
				user.update(phone = json['phone'])

			if 'password' in json and json['password'] != user['password']:
				user.update(password = custom_hash(json['password']))
			
			user.reload()
			user_dict = user.to_mongo().to_dict()
			del user_dict['_id']
			return user_dict, 200

		except NotUniqueError as e:
			return {"type":"NotUniqueError","err":str(e)}, 400

		except ValidationError as e:
			return {"type":"ValidationError", 'err':e.to_dict()}, 400

		except Exception as e:
			return {"type":"Exception","err": str(e)}, 400
