from flask_restful import Resource
from flask import request
from mongoengine.errors import NotUniqueError, ValidationError, DoesNotExist
from bson.objectid import ObjectId

from models import Recruiter
from api.utils import abort_if_invalid_request_params, me_obj_to_serializable, exception_decorator


class RecruiterApi(Resource):

	@exception_decorator((DoesNotExist, Exception))
	def get(self):
		args = request.args

		if 'id' in args:
			return me_obj_to_serializable(Recruiter.objects.get(id=args['id']))
		elif 'email' in args:
			return me_obj_to_serializable(Recruiter.objects.get(email=args['email']))
		elif 'phone' in args:
			return me_obj_to_serializable(Recruiter.objects.get(phone=args['phone']))
		else:
			return me_obj_to_serializable(Recruiter.objects)


	@exception_decorator((NotUniqueError, ValidationError, Exception))
	def post(self):
		json = request.json
		abort_if_invalid_request_params(json, ['first_name', 'last_name', 'email', 'phone', 'password', 'organization'])

		recruiter = Recruiter()
		recruiter.first_name = json['first_name']
		recruiter.last_name = json['last_name']
		recruiter.email = json['email']
		recruiter.phone = json['phone']
		recruiter.password = custom_hash(json['password'])
		recruiter.organization = json['organization']
		recruiter.save()
		
		return me_obj_to_serializable(recruiter)


	@exception_decorator((DoesNotExist, NotUniqueError, ValidationError, Exception))
	def put(self):
		json = request.json

		if 'id' in json:
			recruiter = Recruiter.objects.get(id=json['id'])
		elif '_email'in json:
			recruiter = Recruiter.objects.get(email=json['_email'])
		else:
			abort_if_invalid_request_params(json, ['id', '_email'])

		if 'first_name' in json and json['first_name'] != recruiter['first_name']:
			recruiter.update(first_name = json['first_name'])

		if 'last_name' in json and json['last_name'] != recruiter['last_name']:
			recruiter.update(last_name = json['last_name'])

		if 'email' in json and json['email'] != recruiter['email']:
			recruiter.update(email = json['email'])

		if 'phone' in json and json['phone'] != recruiter['phone']:
			recruiter.update(phone = json['phone'])

		if 'password' in json and json['password'] != recruiter['password']:
			recruiter.update(password = custom_hash(json['password']))
		
		if 'organization' in json and json['organization'] != recruiter['organization']:
			recruiter.update(organization = json['organization'])
		
		recruiter.reload()

		return me_obj_to_serializable(recruiter)


	@exception_decorator((DoesNotExist, NotUniqueError, ValidationError, Exception))
	def delete(self):
		json = request.json
		abort_if_invalid_request_params(json, ['id'])
		Organization.objects.get(id=json['id']).delete()		
		return None		