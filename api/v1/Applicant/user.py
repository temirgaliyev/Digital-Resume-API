from flask_restful import Resource
from flask import request
from mongoengine.errors import NotUniqueError, ValidationError, DoesNotExist

from models import User
from api.utils import abort_if_invalid_request_params, me_obj_to_serializable, exception_decorator, custom_hash


class UserApi(Resource):

	@exception_decorator((DoesNotExist, Exception))
	def get(self):
		args = request.args
		
		if 'id' in args:
			return me_obj_to_serializable(User.objects.get(id=args['id']))
		elif 'email' in args:
			return me_obj_to_serializable(User.objects.get(email=args['email']))
		elif 'phone' in args:
			return me_obj_to_serializable(User.objects.get(phone=args['phone']))
		else:
			return me_obj_to_serializable(User.objects)


	@exception_decorator((NotUniqueError, ValidationError, Exception))
	def post(self):
		json = request.json
		abort_if_invalid_request_params(json, ['first_name', 'last_name', 'email', 'phone', 'password'])

		user = User()
		user.first_name = json['first_name']
		user.last_name = json['last_name']
		user.email = json['email']
		user.phone = json['phone']
		user.password = custom_hash(json['password'])
		user.save()
		
		return me_obj_to_serializable(user)


	@exception_decorator((DoesNotExist, NotUniqueError, ValidationError, Exception))
	def put(self):
		json = request.json

		if 'id' in json:
			user = User.objects.get(id=json['id'])
		elif '_email'in json:
			user = User.objects.get(email=json['_email'])
		else:
			abort_if_invalid_request_params(json, ['id', '_email'])

		if 'first_name' in json and json['first_name'] != user['first_name']:
			user.update(first_name = json['first_name'])

		if 'last_name' in json and json['last_name'] != user['last_name']:
			user.update(last_name = json['last_name'])

		if 'email' in json and json['email'] != user['email']:
			user.update(email = json['email'])

		if 'phone' in json and json['phone'] != user['phone']:
			user.update(phone = json['phone'])

		if 'password' in json and json['password'] != user['password']:
			user.update(password = custom_hash(json['password']))
		
		user.reload()

		return me_obj_to_serializable(user)

	@exception_decorator((DoesNotExist, NotUniqueError, ValidationError, Exception))
	def delete(self):
		json = request.json
		abort_if_invalid_request_params(json, ['id'])
		User.objects.get(id=json['id']).delete()		
		return None		