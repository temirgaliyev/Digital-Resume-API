from flask_restful import Resource
from flask import request
from mongoengine.errors import NotUniqueError, ValidationError, DoesNotExist
from bson.objectid import ObjectId

from models import Experience
from api.utils import abort_if_invalid_request_params, me_obj_to_serializable, exception_decorator


class ExperienceApi(Resource):

	@exception_decorator((DoesNotExist, Exception))
	def get(self):
		args = request.args

		if 'id' in args:
			return me_obj_to_serializable(Experience.objects.get(id=args['id']))
		elif 'user' in args:
			return me_obj_to_serializable(Experience.objects(user=args['user']))
		else:
			return me_obj_to_serializable(Experience.objects)


	@exception_decorator((NotUniqueError, ValidationError, Exception))
	def post(self):

		json = request.json
		abort_if_invalid_request_params(json, ['user', 'position', 'organization', 'job_category', 'date_start', 'date_end', 'country'])

		experience = Experience()
		experience.user = ObjectId(json['user'])		
		experience.position = json['position']
		experience.organization = json['organization']
		experience.job_category = json['job_category']
		experience.date_start = json['date_start']
		experience.date_end = json['date_end']
		experience.country = json['country']
		
		experience.save()
		return me_obj_to_serializable(experience)


	@exception_decorator((DoesNotExist, NotUniqueError, ValidationError, Exception))
	def put(self):
		json = request.json
		abort_if_invalid_request_params(json, ['id'])

		experience = Experience.objects.get(id=json['id'])

		if 'position' in json and json['position'] != experience['position']:
			experience.update(position = json['position'])

		if 'organization' in json and json['organization'] != experience['organization']:
			experience.update(organization = json['organization'])

		if 'job_category' in json and json['job_category'] != experience['job_category']:
			experience.update(job_category = json['job_category'])

		if 'date_start' in json and json['date_start'] != experience['date_start']:
			experience.update(date_start = json['date_start'])

		if 'date_end' in json and json['date_end'] != experience['date_end']:
			experience.update(date_end = custom_hash(json['date_end']))
		
		if 'country' in json and json['country'] != experience['country']:
			experience.update(country = custom_hash(json['country']))
		
		experience.reload()

		return me_obj_to_serializable(experience)
