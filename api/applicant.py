from flask_restful import Resource
from flask import request


attrs = ['first_name', 'last_name', 'email', 'phone']


class User(Resource):
	def get(self):
		return {'hello': 'world'}

	def post(self):
		json = request.get_json(force=True)
		return json
		for attr in attrs:
			if attr not in json:
				return f"Request must contain '{attr}'", 400


		return {'post':'request'}
