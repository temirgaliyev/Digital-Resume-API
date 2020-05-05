from flask_restful import Resource
from flask import request
from mongoengine.errors import NotUniqueError, ValidationError, DoesNotExist
from bson.objectid import ObjectId

from models import Job, JobCategory
from api.utils import abort_if_invalid_request_params, me_obj_to_serializable, exception_decorator

class JobApi(Resource):

	@exception_decorator((DoesNotExist, Exception))
	def get(self):
		args = request.args

		if 'id' in args:
			return me_obj_to_serializable(Job.objects.get(id=args['id']))
		elif 'job' in args:
			return me_obj_to_serializable(Job.objects(job=args['job']))
		elif 'recruiter' in args:
			return me_obj_to_serializable(Job.objects(recruiter=args['recruiter']))
		elif 'position' in args:
			return me_obj_to_serializable(Job.objects(position=args['position']))
		elif 'organization' in args:
			return me_obj_to_serializable(Job.objects(organization=args['organization']))
		elif 'name' in args:
			return me_obj_to_serializable(Job.objects(name=args['name']))
		else:
			return me_obj_to_serializable(Job.objects)


	@exception_decorator((NotUniqueError, ValidationError, Exception))
	def post(self):

		json = request.json
		abort_if_invalid_request_params(json, ['code', 'name', 'description', 'job_category', 'recruiter', 'organization', 'position'])

		job = Job()
		job.code = json['code']
		job.name = json['name']
		job.description = json['description']
		job.job_category = json['job_category']
		job.recruiter = json['recruiter']
		job.organization = json['organization']
		job.position = json['position']
		
		if 'salary_min' in json:
			job.salary_min = json['salary_min']
		
		if 'salary_max' in json:
			job.salary_max = json['salary_max']
		
		if 'currency' in json:
			job.currency = json['currency']


		job.save()
		return me_obj_to_serializable(job)


	@exception_decorator((DoesNotExist, NotUniqueError, ValidationError, Exception))
	def put(self):
		json = request.json

		abort_if_invalid_request_params(json, ['id'])
		job = Job.objects.get(id=json['id'])


		if 'code' in json and json['code'] != job['code']:
			job.update(code = json['code'])

		if 'name' in json and json['name'] != job['name']:
			job.update(name = json['name'])

		if 'description' in json and json['description'] != job['description']:
			job.update(description = json['description'])

		if 'job_category' in json and json['job_category'] != job['job_category']:
			job.update(job_category = json['job_category'])

		if 'recruiter' in json and json['recruiter'] != job['recruiter']:
			job.update(recruiter = json['recruiter'])

		if 'organization' in json and json['organization'] != job['organization']:
			job.update(organization = json['organization'])

		if 'position' in json and json['position'] != job['position']:
			job.update(position = json['position'])

		if 'salary_min' in json and json['salary_min'] != job['salary_min']:
			job.update(salary_min = json['salary_min'])

		if 'salary_max' in json and json['salary_max'] != job['salary_max']:
			job.update(salary_max = json['salary_max'])

		if 'currency' in json and json['currency'] != job['currency']:
			job.update(currency = json['currency'])
		
		if 'is_available' in json and json['is_available'] != job['is_available']:
			job.update(is_available = json['is_available'])
		
		job.reload()

		return me_obj_to_serializable(job)


	@exception_decorator((DoesNotExist, NotUniqueError, ValidationError, Exception))
	def delete(self):
		json = request.json
		abort_if_invalid_request_params(json, ['id'])
		Job.objects.get(id=json['id']).delete()		
		return None
