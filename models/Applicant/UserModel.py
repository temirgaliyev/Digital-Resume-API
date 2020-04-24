from application import mongo
from bson.objectid import ObjectId
from models import BaseModel


def get_model():
	return UserModel


class UserModel(BaseModel):

	def __init__(self, first_name, last_name, email, hashed_password, phone, _id=None):
		self.first_name = first_name        
		self.last_name = last_name
		self.email = email
		self.hashed_password = hashed_password
		self.phone = phone
		self._id = _id


	def __repr__(self):
		return self.first_name + ' ' + self.last_name
	

	@staticmethod	
	def _get_table():
		return mongo.db.users


	@staticmethod	
	def _get_keys_list():
		job_keys_list = ['first_name', 'last_name', 'email', 'hashed_password', 'phone']


	@staticmethod
	def _is_insertable(user):
		is_user_exists = True if get_model().find_by_dict({'$or': [ { 'email':user.email }, { 'phone':user.phone } ]}) else False
		return not is_user_exists
	

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
	def _to_dict(base, with_id=False):
		keys_list = get_model()._get_keys_list()
		_dict = {key:getattr(base, key) for key in keys_list}
		
		if with_id:
			_dict['_id'] = ObjectId(base._id)
		return _dict


	@staticmethod
	def _from_dict(base):
		if base:
			return get_model()(**base)
		
		return None


	@staticmethod
	def insert_from_dict(base):
		if not get_model()._is_insertable(base):
			return False 

		inserted_id = get_model()._get_table().insert_one(base).inserted_id
		return get_model().find_by_id(inserted_id)


	@staticmethod
	def insert_from_model(base):
		return get_model().insert_from_dict(get_model()._to_dict(base))
