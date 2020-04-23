from application import mongo
from bson.objectid import ObjectId
from models import BaseModel

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
	def _to_dict(organization):
		organization_dict = {
			"code": organization.code,
			"name": organization.name,
			"description": organization.description
		}

		return organization_dict


	@staticmethod
	def _is_insertable(organization):
		return OrganizationModel.find_by_dict({'$or': [ { 'code':organization.code }, { 'name':organization.name } ]}) is not None


	# =================================================================================================
	
	@staticmethod
	def find_by_id(_id):
		base_dict = OrganizationModel._get_table().find_one({"_id": ObjectId(_id)})
		return OrganizationModel._from_dict(base_dict)


	@staticmethod
	def find_by_dict(d):
		base_dict = OrganizationModel._get_table().find_one(d)
		return OrganizationModel._from_dict(base_dict)


	@staticmethod
	def _from_dict(base):
		if base:
			return OrganizationModel(**base)
		
		return None


	@staticmethod
	def insert_from_dict(base):
		if not OrganizationModel._is_insertable(base):
			return False 

		inserted_id = OrganizationModel._get_table().insert_one(base).inserted_id
		return OrganizationModel.find_by_id(inserted_id)



	@staticmethod
	def insert_from_model(base):
		return OrganizationModel.insert_from_dict(OrganizationModel._to_dict(base))
