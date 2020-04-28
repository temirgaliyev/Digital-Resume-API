from flask_restful import Resource
from flask import request
from mongoengine.errors import NotUniqueError, ValidationError, DoesNotExist
from bson.objectid import ObjectId

from models import Medcard
from api.utils import abort_if_invalid_request_params, me_obj_to_serializable, exception_decorator


class MedcardApi(Resource):

	@exception_decorator((DoesNotExist, Exception))
	def get(self):
		args = request.args

		if 'id' in args:
			return me_obj_to_serializable(Medcard.objects.get(id=args['id']))
		elif 'user' in args:
			return me_obj_to_serializable(Medcard.objects(user=args['user']))
		else:
			return me_obj_to_serializable(Medcard.objects)


	@exception_decorator((NotUniqueError, ValidationError, Exception))
	def post(self):

		json = request.json
		abort_if_invalid_request_params(json, ['user', 'title', 'url'])

		medcard = Medcard()
		medcard.user = ObjectId(json['user'])			
		medcard.title = json['title']
		medcard.url = json['url']
		
		medcard.save()
		return me_obj_to_serializable(medcard)


	@exception_decorator((DoesNotExist, NotUniqueError, ValidationError, Exception))
	def put(self):
		json = request.json

		abort_if_invalid_request_params(json, ['id'])
		medcard = Medcard.objects.get(id=json['id'])

		if 'title' in json and json['title'] != medcard['title']:
			medcard.update(title = json['title'])

		if 'url' in json and json['url'] != medcard['url']:
			medcard.update(url = json['url'])
		
		medcard.reload()

		return me_obj_to_serializable(medcard)
