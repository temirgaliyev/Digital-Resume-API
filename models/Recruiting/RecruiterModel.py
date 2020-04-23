from application import mongo
from bson.objectid import ObjectId
from models import BaseModel

from models import OrganizationModel

class RecruiterModel(BaseModel):

	def __init__(self, first_name, last_name, organization_id, email, phone, _id=None):
		self.first_name = first_name        
		self.last_name = last_name
		self.organization_id = organization_id
		self.email = email
		self.phone = phone
		self._id = None


	def __repr__(self):
		return self.first_name + ' ' + self.last_name
	

	@staticmethod	
	def _get_table():
		return mongo.db.recruiters


	@staticmethod
	def _to_dict(recruiter):
		recruiter_dict = {
			"first_name": recruiter.first_name,
			"last_name": recruiter.last_name,
			"organization_id": recruiter.organization_id,
			"email": recruiter.email,
			"phone": recruiter.phone
		}

		return recruiter_dict


	@staticmethod
	def _is_insertable(recruiter):
		is_recruiter_exists = True if RecruiterModel.find_by_dict({'$or': [ { 'email':recruiter.email }, { 'phone':recruiter.phone } ]}) else False
		is_organization_exists = True if OrganizationModel.find_by_id(recruiter.organization_id) else False
		return  not is_recruiter_exists and is_organization_exists
	

	@staticmethod
	def find_by_email(email):
		return RecruiterModel.find_by_dict({"email": email})


	# =================================================================================================

	@staticmethod
	def find_by_id(_id):
		base_dict = RecruiterModel._get_table().find_one({"_id": ObjectId(_id)})
		return RecruiterModel._from_dict(base_dict)


	@staticmethod
	def find_by_dict(d):
		base_dict = RecruiterModel._get_table().find_one(d)
		return RecruiterModel._from_dict(base_dict)


	@staticmethod
	def _from_dict(base):
		if base:
			return RecruiterModel(**base)
		
		return None


	@staticmethod
	def insert_from_dict(base):
		if not RecruiterModel._is_insertable(base):
			return False 

		inserted_id = RecruiterModel._get_table().insert_one(base).inserted_id
		return RecruiterModel.find_by_id(inserted_id)



	@staticmethod
	def insert_from_model(base):
		return RecruiterModel.insert_from_dict(RecruiterModel._to_dict(base))
