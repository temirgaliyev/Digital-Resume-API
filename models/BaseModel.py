from application import mongo
from bson.objectid import ObjectId
from abc import ABC, abstractmethod


def get_model():
	return BaseModel


class BaseModel(ABC):

	def __init__(self, _id=None):
		self._id = _id


	def __repr__(self):
		raise NotImplementedError("Method '__repr__' must be overrided")
	

	@staticmethod	
	@abstractmethod
	def _get_table():
		raise NotImplementedError("Method '_get_table' must be overrided")


	@staticmethod	
	@abstractmethod
	def _get_keys_list():
		raise NotImplementedError("Method '_get_keys_list' must be overrided")


	@staticmethod
	@abstractmethod
	def _is_insertable(base):
		raise NotImplementedError("Method '_is_insertable' must be overrided")


	# ===================================================================================

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
