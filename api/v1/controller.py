from flask import Blueprint
from flask_restful import Api

from api.v1.Applicant import *

controller = Blueprint('v1', __name__)
api = Api(controller)

api.add_resource(UserApi, '/user', '/user/')
api.add_resource(ExperienceApi, '/experience', '/experience/')
api.add_resource(EducationApi, '/education', '/education/')
api.add_resource(CertificateApi, '/certificate', '/certificate/')
api.add_resource(MedcardApi, '/medcard', '/medcard/')

api.add_resource(ResumeApi, '/resume', '/resume/')
api.add_resource(ResumeCertificatesApi, '/resume/certificates', '/resume/certificates/')

# '/resume', '/resume/'
		# /create (standart)
		# /delete (many by user, one by id)
		# /get (many by user, one by id) 
		# /update (summary)


# /resume/experiences?id # append/delete
# /resume/{id}/educations # append/delete
# /resume/{id}/medcards # append/delete
# /resume/{id}/certificates # append/delete
