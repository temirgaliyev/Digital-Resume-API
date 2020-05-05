from flask_restful import Resource
from flask import request
from mongoengine.errors import NotUniqueError, ValidationError, DoesNotExist
from bson.objectid import ObjectId

from models import Organization
from api.utils import abort_if_invalid_request_params, me_obj_to_serializable, exception_decorator


class OrganizationApi(Resource):

	@exception_decorator((DoesNotExist, Exception))
	def get(self):
		args = request.args

		if 'id' in args:
			return me_obj_to_serializable(Organization.objects.get(id=args['id']))
		elif 'code' in args:
			return me_obj_to_serializable(Organization.objects(code=args['code']))
		else:
			return me_obj_to_serializable(Organization.objects)


	@exception_decorator((NotUniqueError, ValidationError, Exception))
	def post(self):

		json = request.json
		abort_if_invalid_request_params(json, ['code', 'name'])

		organization = Organization()
		organization.code = json['code']
		organization.name = json['name']
		
		if 'description' in json:
			organization.description = json['description']
	

		organization.save()
		return me_obj_to_serializable(organization)


	@exception_decorator((DoesNotExist, NotUniqueError, ValidationError, Exception))
	def put(self):
		json = request.json

		if 'id' in json:
			organization = Organization.objects.get(id=json['id'])
		elif '_code' in json:
			organization = Organization.objects.get(code=json['_code'])
		else:
			abort_if_invalid_request_params(json, ['id', '_code'])


		if 'code' in json and json['code'] != organization['code']:
			organization.update(code = json['code'])

		if 'name' in json and json['name'] != organization['name']:
			organization.update(name = json['name'])

		if 'description' in json and json['description'] != organization['description']:
			organization.update(description = json['description'])

		organization.reload()

		return me_obj_to_serializable(organization)


	@exception_decorator((DoesNotExist, NotUniqueError, ValidationError, Exception))
	def delete(self):
		json = request.json
		abort_if_invalid_request_params(json, ['id'])
		Organization.objects.get(id=json['id']).delete()		
		return None		