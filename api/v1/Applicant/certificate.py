from flask_restful import Resource
from flask import request
from mongoengine.errors import NotUniqueError, ValidationError, DoesNotExist
from bson.objectid import ObjectId

from models import Certificate
from api.utils import abort_if_invalid_request_params, me_obj_to_serializable, exception_decorator


class CertificateApi(Resource):

	@exception_decorator((DoesNotExist, Exception))
	def get(self):
		args = request.args

		if 'id' in args:
			return me_obj_to_serializable(Certificate.objects.get(id=args['id']))
		elif 'user' in args:
			return me_obj_to_serializable(Certificate.objects(user=args['user']))
		else:
			return me_obj_to_serializable(Certificate.objects)


	@exception_decorator((NotUniqueError, ValidationError, Exception))
	def post(self):

		json = request.json
		abort_if_invalid_request_params(json, ['user', 'title', 'description', 'url'])

		certificate = Certificate()
		certificate.user = ObjectId(json['user'])			
		certificate.title = json['title']
		certificate.description = json['description']
		certificate.url = json['url']
		
		certificate.save()
		return me_obj_to_serializable(certificate)


	@exception_decorator((DoesNotExist, NotUniqueError, ValidationError, Exception))
	def put(self):
		json = request.json

		abort_if_invalid_request_params(json, ['id'])
		certificate = Certificate.objects.get(id=json['id'])

		if 'title' in json and json['title'] != certificate['title']:
			certificate.update(title = json['title'])

		if 'description' in json and json['description'] != certificate['description']:
			certificate.update(description = json['description'])

		if 'url' in json and json['url'] != certificate['url']:
			certificate.update(url = json['url'])
		
		certificate.reload()

		return me_obj_to_serializable(certificate)
