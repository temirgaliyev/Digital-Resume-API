from application import mongo
from bson.objectid import ObjectId
from models import BaseModel, OrganizationModel


def get_model():
	return RecruiterModel

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
	def _get_keys_list():
		job_keys_list = ['first_name', 'last_name', 'organization_id', 'email', 'phone']


	@staticmethod
	def _is_insertable(recruiter):
		is_recruiter_exists = True if get_model().find_by_dict({'$or': [ { 'email':recruiter.email }, { 'phone':recruiter.phone } ]}) else False
		if is_recruiter_exists:
			return False, 'recruiter already exists'

		is_organization_exists = True if OrganizationModel.find_by_id(recruiter.organization_id) else False
		if not is_organization_exists:
			return False, 'organization does not exist'

		return True
	

	@staticmethod
	def find_by_email(email):
		return get_model().find_by_dict({"email": email})


	# =================================================================================================

	@staticmethod
	def find_by_id(_id):
		base_dict = get_model()._get_table().find_one({"_id": ObjectId(_id)})
		return get_model()._from_dict(base_dict)


	@staticmethod
	def find_by_dict(d):
		base_dict = get_model()._get_table().find_one(d)
		return get_model()._from_dict(base_dict)


	@staticmethod
	def _from_dict(_dict):
		if base:
			return get_model()(**_dict)
		
		return None
	

	@staticmethod
	def _to_dict(base, with_id=False):
		keys_list = get_model()._get_keys_list()
		_dict = {key:getattr(base, key) for key in keys_list}
		
		if with_id:
			_dict['_id'] = ObjectId(base._id)
		return _dict


	@staticmethod
	def insert_from_dict(base):
		if not get_model()._is_insertable(base):
			return False 

		inserted_id = get_model()._get_table().insert_one(base).inserted_id
		return get_model().find_by_id(inserted_id)



	@staticmethod
	def insert_from_model(base):
		return get_model().insert_from_dict(get_model()._to_dict(base))
