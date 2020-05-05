from flask_restful import Resource
from flask import request
from mongoengine.errors import NotUniqueError, ValidationError, DoesNotExist
from bson.objectid import ObjectId

from models import ApplicantEvaluation
from api.utils import abort_if_invalid_request_params, me_obj_to_serializable, exception_decorator


class ApplicantEvaluationApi(Resource):

	@exception_decorator((DoesNotExist, Exception))
	def get(self):
		args = request.args

		if 'id' in args:
			return me_obj_to_serializable(ApplicantEvaluation.objects.get(id=args['id']))
		elif 'recruiter' in args:
			return me_obj_to_serializable(ApplicantEvaluation.objects(recruiter=args['recruiter']))
		else:
			return me_obj_to_serializable(ApplicantEvaluation.objects)


	@exception_decorator((NotUniqueError, ValidationError, Exception))
	def post(self):
		json = request.json
		abort_if_invalid_request_params(json, ['recruiter', 'application'])

		evaluation = ApplicantEvaluation()
		evaluation.recruiter = json['recruiter']
		evaluation.application = json['application']

		if 'notes' in json:
			evaluation.notes = json['notes']

		if 'in_progress' in json:
			evaluation.in_progress = json['in_progress']
		
		if 'hired' in json:
			evaluation.hired = json['hired']
		
		evaluation.save()
		
		return me_obj_to_serializable(evaluation)


	@exception_decorator((DoesNotExist, NotUniqueError, ValidationError, Exception))
	def put(self):
		json = request.json

		if 'id' in json:
			evaluation = ApplicantEvaluation.objects.get(id=json['id'])
		else:
			abort_if_invalid_request_params(json, ['id'])


		if 'recruiter' in json and json['recruiter'] != evaluation['recruiter']:
			evaluation.update(recruiter = json['recruiter'])

		if 'application' in json and json['application'] != evaluation['application']:
			evaluation.update(application = json['application'])

		if 'notes' in json and json['notes'] != evaluation['notes']:
			evaluation.update(notes = json['notes'])

		if 'in_progress' in json and json['in_progress'] != evaluation['in_progress']:
			evaluation.update(in_progress = json['in_progress'])

		if 'hired' in json and json['hired'] != evaluation['hired']:
			evaluation.update(hired = custom_hash(json['hired']))
		
		evaluation.reload()

		return me_obj_to_serializable(evaluation)


	@exception_decorator((DoesNotExist, NotUniqueError, ValidationError, Exception))
	def delete(self):
		json = request.json
		abort_if_invalid_request_params(json, ['id'])
		ApplicantEvaluation.objects.get(id=json['id']).delete()		
		return None		