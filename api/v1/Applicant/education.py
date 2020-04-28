from flask_restful import Resource
from flask import request
from mongoengine.errors import NotUniqueError, ValidationError, DoesNotExist
from bson.objectid import ObjectId

from models import Education
from api.utils import abort_if_invalid_request_params, me_obj_to_serializable, exception_decorator


class EducationApi(Resource):

	@exception_decorator((DoesNotExist, Exception))
	def get(self):
		args = request.args

		if 'id' in args:
			return me_obj_to_serializable(Education.objects.get(id=args['id']))
		elif 'user' in args:
			return me_obj_to_serializable(Education.objects(user=args['user']))
		else:
			return me_obj_to_serializable(Education.objects)


	@exception_decorator((NotUniqueError, ValidationError, Exception))
	def post(self):

		json = request.json
		abort_if_invalid_request_params(json, ['user', 'degree', 'organization', 'date_start', 'date_end', 'country'])

		education = Education()
		education.user = ObjectId(json['user'])			
		education.degree = json['degree']
		education.organization = json['organization']
		education.date_start = json['date_start']
		education.date_end = json['date_end']
		education.country = json['country']
		
		education.save()
		return me_obj_to_serializable(education)


	@exception_decorator((DoesNotExist, NotUniqueError, ValidationError, Exception))
	def put(self):
		json = request.json

		abort_if_invalid_request_params(json, ['id'])
		education = Education.objects.get(id=json['id'])

		if 'degree' in json and json['degree'] != education['degree']:
			education.update(degree = json['degree'])

		if 'organization' in json and json['organization'] != education['organization']:
			education.update(organization = json['organization'])

		if 'date_start' in json and json['date_start'] != education['date_start']:
			education.update(date_start = json['date_start'])

		if 'date_end' in json and json['date_end'] != education['date_end']:
			education.update(date_end = custom_hash(json['date_end']))
		
		if 'country' in json and json['country'] != education['country']:
			education.update(country = custom_hash(json['country']))
		
		education.reload()

		return me_obj_to_serializable(education)
