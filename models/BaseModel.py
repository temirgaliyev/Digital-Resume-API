from application import mongo
from bson.objectid import ObjectId
from abc import ABC, abstractmethod

class BaseModel(ABC):

	def __init__(self):
		pass

	def __repr__(self):
		raise NotImplementedError("Method '__repr__' must be overrided")
	

	@staticmethod	
	@abstractmethod
	def _get_table():
		raise NotImplementedError("Method '_get_table' must be overrided")


	@staticmethod
	@abstractmethod
	def _to_dict(user):
		raise NotImplementedError("Method '_to_dict' must be overrided")


	@staticmethod
	@abstractmethod
	def _is_insertable(base):
		raise NotImplementedError("Method '_is_insertable' must be overrided")


	@staticmethod
	@abstractmethod
	def find_by_id(_id):
		base_dict = BaseModel._get_table().find_one({"_id": ObjectId(_id)})
		return BaseModel._from_dict(base_dict)


	@staticmethod
	@abstractmethod
	def find_by_dict(d):
		base_dict = BaseModel._get_table().find_one(d)
		return BaseModel._from_dict(base_dict)


	@staticmethod
	@abstractmethod
	def _from_dict(base):
		if base:
			return BaseModel(**base)
		
		return None


	@staticmethod
	@abstractmethod
	def insert_from_dict(base):
		if not BaseModel._is_insertable(base):
			return False 

		inserted_id = BaseModel._get_table().insert_one(base).inserted_id
		return BaseModel.find_by_id(inserted_id)



	@staticmethod
	@abstractmethod
	def insert_from_model(base):
		return BaseModel.insert_from_dict(BaseModel._to_dict(base))
