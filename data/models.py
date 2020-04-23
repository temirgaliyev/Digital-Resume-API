from application import mongo
from bson.objectid import ObjectId

class User():

	def __init__(self, first_name, last_name, email, hashed_password, phone, _id=None):
		self.first_name = first_name		
		self.last_name = last_name
		self.email = email
		self.hashed_password = hashed_password
		self.phone = phone
		self._id = None


    @staticmethod
    def find_by_id(id):
        user_dict = mongo.db.users.find_one({"_id": ObjectId(id)})
        return User._from_dict(user_dict)


    @staticmethod
    def find_by_email(email):
        user_dict = mongo.db.users.find_one({"email": email})
        retun User._from_dict(user_dict)


    @staticmethod
    def _from_dict(user):
        if user:
            return User(first_name=user.get('first_name', ''), 
            	last_name=user.get('last_name', ''), 
            	email=user.get('email', ''), 
            	hashed_password=user.get('hashed_password', ''),
            	phone=user.get('phone', ''),
            	_id=user.get('_id', ''))
        else:
            return None


	@staticmethod
	def insert(user):
		if User.find_by_email(user.email): # email already exists
			return False 

        inserted_id = mongo.db.users.insert_one({
        	"first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "hashed_password": user.hashed_password,
            "phone": user.phone
        }).inserted_id
        
        return User.find_by_id(inserted_id)
