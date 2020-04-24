from application import mongo
from bson.objectid import ObjectId
from models import BaseModel, JobCategoryModel, RecruiterModel

class JobModel(BaseModel):

	def __init__(self, 
			name, description, job_category_id, recruiter_id, 
			position, salary_min, salary_max, currency, status, 
			date_published=None, _id=None):

		self.name = name
		self.description = description
		self.job_category_id = job_category_id
		self.recruiter_id = recruiter_id
		self.position = position
		self.salary_min = salary_min
		self.salary_max = salary_max
		self.currency = currency
		self.status = status
		self.date_published = date_published
		self._id = _id


	def __repr__(self):
		return self.name + ' ' + self.position
	

	@staticmethod	
	def _get_table():
		return mongo.db.jobs


	@staticmethod	
	def _get_keys_list():
		job_keys_list = ['name', 'description', 'job_category_id', 'recruiter_id', 'position', 'salary_min', 'salary_max', 'currency', 'status', 'date_published']


	@staticmethod
	def _is_insertable(job):
		job_category_id_exists = True if JobCategoryModel.find_by_id(job.job_category_id) else False
		
		if not job_category_id_exists:
			return False, 'Job is not exists'

		recruiter_exists = True if RecruiterModel.find_by_id(job.recruiter_id) else False
		
		if not recruiter_exists:
			return False, 'Recruiter is not exists'

		return True
	

	# =================================================================================================

	@staticmethod
	def find_by_id(_id):
		base_dict = JobModel._get_table().find_one({"_id": ObjectId(_id)})
		return JobModel._from_dict(base_dict)


	@staticmethod
	def find_by_dict(d):
		base_dict = JobModel._get_table().find_one(d)
		return JobModel._from_dict(base_dict)


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
		if not JobModel._is_insertable(base):
			return False 

		inserted_id = JobModel._get_table().insert_one(base).inserted_id
		return JobModel.find_by_id(inserted_id)


	@staticmethod
	def insert_from_model(base):
		return JobModel.insert_from_dict(JobModel._to_dict(base))
