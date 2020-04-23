from application import mongo
from bson.objectid import ObjectId
from models import BaseModel

class UserModel(BaseModel):

	def __init__(self, first_name, last_name, email, hashed_password, phone, _id=None):
		self.first_name = first_name        
		self.last_name = last_name
		self.email = email
		self.hashed_password = hashed_password
		self.phone = phone
		self._id = None


	def __repr__(self):
		return self.first_name + ' ' + self.last_name
	

	@staticmethod	
	def _get_table():
		return mongo.db.users


	@staticmethod
	def _to_dict(user):
		user_dict = {
			"first_name": user.first_name,
			"last_name": user.last_name,
			"email": user.email,
			"hashed_password": user.hashed_password,
			"phone": user.phone
		}

		return user_dict


	@staticmethod
	def _is_insertable(user):
		is_user_exists = True if UserModel.find_by_dict({'$or': [ { 'email':user.email }, { 'phone':user.phone } ]}) else False
		return not is_user_exists
	

	@staticmethod
	def find_by_email(email):
		return UserModel.find_by_dict({"email": email})


	# =================================================================================================

	@staticmethod
	def find_by_id(_id):
		base_dict = UserModel._get_table().find_one({"_id": ObjectId(_id)})
		return UserModel._from_dict(base_dict)


	@staticmethod
	def find_by_dict(d):
		base_dict = UserModel._get_table().find_one(d)
		return UserModel._from_dict(base_dict)


	@staticmethod
	def _from_dict(base):
		if base:
			return UserModel(**base)
		
		return None


	@staticmethod
	def insert_from_dict(base):
		if not UserModel._is_insertable(base):
			return False 

		inserted_id = UserModel._get_table().insert_one(base).inserted_id
		return UserModel.find_by_id(inserted_id)



	@staticmethod
	def insert_from_model(base):
		return UserModel.insert_from_dict(UserModel._to_dict(base))
