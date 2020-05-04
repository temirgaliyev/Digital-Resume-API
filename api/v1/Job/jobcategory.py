from flask_restful import Resource
from flask import request
from mongoengine.errors import NotUniqueError, ValidationError, DoesNotExist
from bson.objectid import ObjectId

from models import JobCategory
from api.utils import abort_if_invalid_request_params, me_obj_to_serializable, exception_decorator

class JobCategoryApi(Resource):

	@exception_decorator((DoesNotExist, Exception))
	def get(self):
		args = request.args

		if 'id' in args:
			return me_obj_to_serializable(JobCategory.objects.get(id=args['id']))
		elif 'code' in args:
			return me_obj_to_serializable(JobCategory.objects.get(id=args['code']))
		else:
			return me_obj_to_serializable(JobCategory.objects)


	@exception_decorator((NotUniqueError, ValidationError, Exception))
	def post(self):

		json = request.json
		abort_if_invalid_request_params(json, ['code', 'name'])

		job_category = JobCategory()
		job_category.code = json['code']			
		job_category.name = json['name']
		if 'description' in json:
			job_category.description = json['description']
		
		job_category.save()
		return me_obj_to_serializable(job_category)


	@exception_decorator((DoesNotExist, NotUniqueError, ValidationError, Exception))
	def put(self):
		json = request.json

		if 'id' in json:
			job_category = JobCategory.objects.get(id=json['id'])
		elif '_code' in json:
			job_category = JobCategory.objects.get(code=json['_code'])
		elif '_name' in json:
			job_category = JobCategory.objects.get(name=json['_name'])
		else:
			abort_if_invalid_request_params(json, ['id', '_code', '_name'])


		if 'code' in json and json['code'] != job_category['code']:
			job_category.update(code = json['code'])

		if 'name' in json and json['name'] != job_category['name']:
			job_category.update(name = json['name'])

		if 'description' in json and json['description'] != job_category['description']:
			job_category.update(description = json['description'])

		
		job_category.reload()

		return me_obj_to_serializable(job_category)


	@exception_decorator((DoesNotExist, NotUniqueError, ValidationError, Exception))
	def delete(self):
		json = request.json

		if 'id' in json:
			JobCategory.objects.get(id=json['id']).delete()
		elif '_code' in json:
			JobCategory.objects.get(code=json['_code']).delete()
		elif 'code' in json:
			JobCategory.objects.get(code=json['code']).delete()
		elif '_name' in json:
			JobCategory.objects.get(name=json['_name']).delete()
		elif 'name' in json:
			JobCategory.objects.get(name=json['name']).delete()
		else:
			abort_if_invalid_request_params(json, ['id', '_code', 'code', '_name', 'name'])
		
		return None
