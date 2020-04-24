from application import mongo
from bson.objectid import ObjectId
from models import BaseModel


def get_model():
	return OrganizationModel


class OrganizationModel(BaseModel):

	def __init__(self, code, name, description, _id=None):
		self.code = code
		self.name = name
		self.description = description
		self._id = None


	def __repr__(self):
		return self.code + '. ' + self.name
	

	@staticmethod	
	def _get_table():
		return mongo.db.organizations


	@staticmethod	
	def _get_keys_list():
		job_keys_list = ['code', 'name', 'description']
		return job_keys_list


	@staticmethod
	def _is_insertable(organization):
		condition = {'$or': [ { 'code':organization.code }, { 'name':organization.name } ]}
		is_org_exists = True if get_model().find_by_dict(condition) else False
		if is_org_exists:
			return False, "organization already exists"

		return True


	# =================================================================================================
	
	@staticmethod
	def find_by_id(_id):
		base_dict = get_model()._get_table().find_one({"_id": ObjectId(_id)})
		return get_model()._from_dict(base_dict)


	@staticmethod
	def find_by_dict(_dict):
		base_dict = get_model()._get_table().find_one(_dict)
		return get_model()._from_dict(base_dict)


	@staticmethod
	def _to_dict(base, with_id=False):
		keys_list = get_model()._get_keys_list()
		_dict = {key:getattr(base, key) for key in keys_list}
		
		if with_id:
			_dict['_id'] = ObjectId(base._id)
		return _dict


	@staticmethod
	def _from_dict(_dict):
		if _dict:
			return get_model()(**_dict)
		
		return None


	@staticmethod
	def insert_from_dict(_dict):
		if not get_model()._is_insertable(_dict):
			return False 

		inserted_id = get_model()._get_table().insert_one(_dict).inserted_id
		return get_model().find_by_id(inserted_id)


	@staticmethod
	def insert_from_model(base):
		return get_model().insert_from_dict(get_model()._to_dict(base))
