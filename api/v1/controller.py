from flask import Blueprint
from flask_restful import Api

from api.v1.Applicant import *
from api.v1.Job import *
from api.v1.Recruiting import *
from api.v1.Application import *

controller = Blueprint('v1', __name__)
api = Api(controller)

# Applicant
api.add_resource(UserApi, '/user', '/user/')
api.add_resource(ExperienceApi, '/experience', '/experience/')
api.add_resource(EducationApi, '/education', '/education/')
api.add_resource(MedcardApi, '/medcard', '/medcard/')
api.add_resource(CertificateApi, '/certificate', '/certificate/')

api.add_resource(ResumeApi, '/resume', '/resume/')
api.add_resource(ResumeExperiencesApi, '/resume/experiences', '/resume/experiences/')
api.add_resource(ResumeEducationsApi, '/resume/educations', '/resume/educations/')
api.add_resource(ResumeMedcardsApi, '/resume/medcards', '/resume/medcards/')
api.add_resource(ResumeCertificatesApi, '/resume/certificates', '/resume/certificates/')

# ==========================================


# Job
api.add_resource(JobApi, '/job', '/job/')
api.add_resource(JobCategoryApi, '/jobcategory', '/jobcategory/')

# ==========================================


# Recruiting
api.add_resource(OrganizationApi, '/organization', '/organization/')
api.add_resource(RecruiterApi, '/recruiter', '/recruiter/')
api.add_resource(ApplicantEvaluationApi, '/evaluation', '/evaluation/')

# ==========================================


# Application
api.add_resource(ApplicationApi, '/application', '/application/')

# ==========================================
