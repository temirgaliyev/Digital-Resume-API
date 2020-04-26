from flask import Blueprint
from flask_restful import Api
from api.v1.applicant import UserApi

controller = Blueprint('v1', __name__)
api = Api(controller)

api.add_resource(UserApi, '/user', '/user/')
