from flask import Blueprint
from mongoengine.errors import NotUniqueError, DoesNotExist
# from application import mongo

test_blueprint = Blueprint('test', __name__)

@test_blueprint.route("")
def home():
	return str("Not implemented")
	# return str(mongo.db)

	# from models import UserModel
	# user = UserModel('Arystan', 'Amanzholov', 'arysisthebest@2k.20', hash('arysisthebest'), '+77bestphone')
	# user_insert_response = UserModel.insert_from_model(user)
	# return str(user_insert_response)

	# from models import OrganizationModel
	# organization = OrganizationModel('code', 'name', 'description')
	# organization_insert_response = OrganizationModel.insert_from_model(organization)
	# return str(organization_insert_response)
# 
	# from models import User

	# try:
	# 	user = User(first_name='First', last_name='Last', email='Email@ma.ru', phone='Phone')
	# 	user.save()
	# 	return str(user)
	# except NotUniqueError as error:
	# 	return str(error)

	# try:
	# 	return User.objects.get(email='Email@ma.ru')
	# except DoesNotExist as e:
	# 	return str(e)


		

	# from models import RecruiterModel, OrganizationModel
	# organization = OrganizationModel.find_by_code('code')
	# print("TEST:CONTROLLERS: organization:", organization)
	# recruiter = RecruiterModel('first_name', 'last_name', organization._id, 'email', 'phone')
	# recruiter = RecruiterModel.insert_from_model(recruiter)
	# return str(recruiter)
