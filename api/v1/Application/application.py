from flask_restful import Resource
from flask import request
from mongoengine.errors import NotUniqueError, ValidationError, DoesNotExist
from bson.objectid import ObjectId

from models import Application
from api.utils import abort_if_invalid_request_params, me_obj_to_serializable, exception_decorator


class ApplicationApi(Resource):

	@exception_decorator((DoesNotExist, Exception))
	def get(self):
		args = request.args

		if 'id' in args:
			return me_obj_to_serializable(Application.objects.get(id=args['id']))
		elif 'job' in args:
			return me_obj_to_serializable(Application.objects(job=args['job']))
		elif 'resume' in args:
			return me_obj_to_serializable(Application.objects(resume=args['resume']))
		else:
			return me_obj_to_serializable(Application.objects)


	@exception_decorator((NotUniqueError, ValidationError, Exception))
	def post(self):
		json = request.json
		abort_if_invalid_request_params(json, ['job', 'resume'])

		application = Application()
		application.job = json['job']
		application.resume = json['resume']

		if 'cover_letter' in json:
			application.cover_letter = json['cover_letter']
		
		application.save()
		
		return me_obj_to_serializable(application)


	@exception_decorator((DoesNotExist, NotUniqueError, ValidationError, Exception))
	def put(self):
		json = request.json

		abort_if_invalid_request_params(json, ['id'])
		application = Application.objects.get(id=json['id'])

		if 'job' in json and json['job'] != application['job']:
			application.update(job = json['job'])

		if 'resume' in json and json['resume'] != application['resume']:
			application.update(resume = json['resume'])

		if 'cover_letter' in json and json['cover_letter'] != application['cover_letter']:
			application.update(cover_letter = json['cover_letter'])
		
		application.reload()

		return me_obj_to_serializable(application)


	@exception_decorator((DoesNotExist, NotUniqueError, ValidationError, Exception))
	def delete(self):
		json = request.json
		abort_if_invalid_request_params(json, ['id'])
		Application.objects.get(id=json['id']).delete()		
		return None		