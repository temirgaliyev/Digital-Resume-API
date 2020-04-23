from application import mongo
from bson.objectid import ObjectId
from models import BaseModel

class JobCategoryModel(BaseModel):

	def __init__(self, code, name, description, _id=None):
		self.code = code
		self.name = name
		self.description = description
		self._id = None


	def __repr__(self):
		return self.code + '. ' + self.name
	

	@staticmethod	
	def _get_table():
		return mongo.db.job_categories


	@staticmethod
	def _to_dict(job_category):
		job_category_dict = {
			"code": job_category.code,
			"name": job_category.name,
			"description": job_category.description
		}

		return job_category_dict


	@staticmethod
	def _is_insertable(job_category):
		return JobCategoryModel.find_by_dict({'$or': [ { 'code':job_category.code }, { 'name':job_category.name } ]}) is not None


	# =================================================================================================
	
	@staticmethod
	def find_by_id(_id):
		base_dict = JobCategoryModel._get_table().find_one({"_id": ObjectId(_id)})
		return JobCategoryModel._from_dict(base_dict)


	@staticmethod
	def find_by_dict(d):
		base_dict = JobCategoryModel._get_table().find_one(d)
		return JobCategoryModel._from_dict(base_dict)


	@staticmethod
	def _from_dict(base):
		if base:
			return JobCategoryModel(**base)
		
		return None


	@staticmethod
	def insert_from_dict(base):
		if not JobCategoryModel._is_insertable(base):
			return False 

		inserted_id = JobCategoryModel._get_table().insert_one(base).inserted_id
		return JobCategoryModel.find_by_id(inserted_id)



	@staticmethod
	def insert_from_model(base):
		return JobCategoryModel.insert_from_dict(JobCategoryModel._to_dict(base))
