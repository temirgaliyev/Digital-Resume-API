from flask_restful import Resource
from flask import request
from mongoengine.errors import NotUniqueError, ValidationError, DoesNotExist
from bson.objectid import ObjectId

from models import Resume
from api.utils import abort_if_invalid_request_params, me_obj_to_serializable, exception_decorator


class ResumeApi(Resource):

	@exception_decorator((DoesNotExist, Exception))
	def get(self):
		args = request.args

		if 'id' in args:
			return me_obj_to_serializable(Resume.objects.get(id=args['id']))
		elif 'user' in args:
			return me_obj_to_serializable(Resume.objects(user=args['user']))
		else:
			return me_obj_to_serializable(Resume.objects)


	@exception_decorator((NotUniqueError, ValidationError, Exception))
	def post(self):

		json = request.json
		abort_if_invalid_request_params(json, ['user'])

		resume = Resume()
		resume.user = ObjectId(json['user'])

		if 'experiences' in json:
			resume.experiences = [ObjectId(_id) for _id in json['experiences']]
		
		if 'educations' in json:
			resume.educations = [ObjectId(_id) for _id in json['educations']]
		
		if 'medcards' in json:
			resume.medcards = [ObjectId(_id) for _id in json['medcards']]
		
		if 'certificates' in json:
			resume.certificates = [ObjectId(_id) for _id in json['certificates']]
		
		if 'summary' in json:
			resume.summary = json['summary']

		resume.save()
		return me_obj_to_serializable(resume)


	@exception_decorator((DoesNotExist, NotUniqueError, ValidationError, Exception))
	def put(self):
		json = request.json

		abort_if_invalid_request_params(json, ['id', 'summary'])
		resume = Resume.objects.get(id=json['id'])
		resume.update(summary = json['summary'])		
		resume.reload()

		return me_obj_to_serializable(resume)


	@exception_decorator((DoesNotExist, NotUniqueError, ValidationError, Exception))
	def delete(self):
		json = request.json
		abort_if_invalid_request_params(json, ['id'])

		Resume.objects.get(id=json['id']).delete()

		return None


class ResumeExperiencesApi(Resource):
	
	@exception_decorator((DoesNotExist, Exception))
	def get(self):
		args = request.args
		abort_if_invalid_request_params(args, ['id'])
		return me_obj_to_serializable(Resume.objects.get(id=args['id'])['experiences'])


	@exception_decorator((NotUniqueError, ValidationError, Exception))
	def post(self):

		json = request.json
		abort_if_invalid_request_params(json, ['id' ,'experiences'])

		resume = Resume.objects.get(id=json['id'])
		for _id in json['experiences']:
			resume.update(add_to_set__experiences=ObjectId(_id))
		resume.reload()

		return me_obj_to_serializable(resume)


	@exception_decorator((DoesNotExist, ValidationError, Exception))
	def delete(self):
		json = request.json
		abort_if_invalid_request_params(json, ['id' ,'experiences'])

		resume = Resume.objects.get(id=json['id'])
		for _id in json['experiences']:
			resume.update(pull__experiences=ObjectId(_id))
		resume.reload()
		
		return me_obj_to_serializable(resume)


class ResumeEducationsApi(Resource):
	
	@exception_decorator((DoesNotExist, Exception))
	def get(self):
		args = request.args
		abort_if_invalid_request_params(args, ['id'])
		return me_obj_to_serializable(Resume.objects.get(id=args['id'])['educations'])


	@exception_decorator((NotUniqueError, ValidationError, Exception))
	def post(self):

		json = request.json
		abort_if_invalid_request_params(json, ['id' ,'educations'])

		resume = Resume.objects.get(id=json['id'])
		for _id in json['educations']:
			resume.update(add_to_set__educations=ObjectId(_id))
		resume.reload()

		return me_obj_to_serializable(resume)


	@exception_decorator((DoesNotExist, ValidationError, Exception))
	def delete(self):
		json = request.json
		abort_if_invalid_request_params(json, ['id' ,'educations'])

		resume = Resume.objects.get(id=json['id'])
		for _id in json['educations']:
			resume.update(pull__educations=ObjectId(_id))
		resume.reload()
		
		return me_obj_to_serializable(resume)


class ResumeCertificatesApi(Resource):
	
	@exception_decorator((DoesNotExist, Exception))
	def get(self):
		args = request.args
		abort_if_invalid_request_params(args, ['id'])
		return me_obj_to_serializable(Resume.objects.get(id=args['id'])['certificates'])


	@exception_decorator((NotUniqueError, ValidationError, Exception))
	def post(self):

		json = request.json
		abort_if_invalid_request_params(json, ['id' ,'certificates'])

		resume = Resume.objects.get(id=json['id'])
		for _id in json['certificates']:
			resume.update(add_to_set__certificates=ObjectId(_id))
		resume.reload()

		return me_obj_to_serializable(resume)


	@exception_decorator((DoesNotExist, ValidationError, Exception))
	def delete(self):
		json = request.json
		abort_if_invalid_request_params(json, ['id' ,'certificates'])

		resume = Resume.objects.get(id=json['id'])
		for _id in json['certificates']:
			resume.update(pull__certificates=ObjectId(_id))
		resume.reload()
		
		return me_obj_to_serializable(resume)



class ResumeMedcardsApi(Resource):
	
	@exception_decorator((DoesNotExist, Exception))
	def get(self):
		args = request.args
		abort_if_invalid_request_params(args, ['id'])
		return me_obj_to_serializable(Resume.objects.get(id=args['id'])['medcards'])


	@exception_decorator((NotUniqueError, ValidationError, Exception))
	def post(self):

		json = request.json
		abort_if_invalid_request_params(json, ['id' ,'medcards'])

		resume = Resume.objects.get(id=json['id'])
		for _id in json['medcards']:
			resume.update(add_to_set__medcards=ObjectId(_id))
		resume.reload()

		return me_obj_to_serializable(resume)


	@exception_decorator((DoesNotExist, ValidationError, Exception))
	def delete(self):
		json = request.json
		abort_if_invalid_request_params(json, ['id' ,'medcards'])

		resume = Resume.objects.get(id=json['id'])
		for _id in json['medcards']:
			resume.update(pull__medcards=ObjectId(_id))
		resume.reload()
		
		return me_obj_to_serializable(resume)
