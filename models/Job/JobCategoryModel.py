from application import mongo
from bson.objectid import ObjectId
from models import BaseModel


def get_model():
	return JobCategoryModel


class JobCategoryModel(BaseModel):

	def __init__(self, code, name, description, _id=None):
		self.code = code
		self.name = name
		self.description = description
		self._id = _id


	def __repr__(self):
		return self.code + '. ' + self.name
	

	@staticmethod	
	def _get_table():
		return mongo.db.job_categories


	@staticmethod	
	def _get_keys_list():
		job_keys_list = ['code', 'name', 'description']


	@staticmethod
	def _is_insertable(job_category):
		return get_model().find_by_dict({'$or': [ { 'code':job_category.code }, { 'name':job_category.name } ]}) is None


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
