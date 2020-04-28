from hashlib import md5, sha256
from flask import abort

from mongoengine import Document 
from mongoengine.queryset import QuerySet
from bson.objectid import ObjectId


def custom_hash(string):
	sha256_encoded = sha256((string).encode('utf-8')).hexdigest()
	md5_encoded = md5((sha256_encoded).encode('utf-8')).hexdigest()
	return md5_encoded


def abort_if_invalid_request_params(_dict, attrs):
	for attr in attrs:
		if attr not in _dict:
			abort(400, f"Request must contain '{attr}'")


def me_obj_to_serializable(obj, need_id=True):
	if isinstance(obj, Document):
		return me_document_to_dict(obj, need_id)
	
	elif isinstance(obj, QuerySet):
		return [me_document_to_dict(val, need_id) for val in obj]

	elif isinstance(obj, list):
		return [me_document_to_dict(_id, need_id) for _id in obj]

	else:
		abort(400, f"'obj' type '{type(obj)}' is incorrect")


def me_document_to_dict(obj, need_id=True):
	if isinstance(obj, Document):
		obj_dict = obj.to_mongo().to_dict()
		if need_id:
			obj_dict['id'] = str(obj_dict.pop('_id'))
		else:
			del obj_dict['_id']

		for key, value in obj_dict.items():
			if isinstance(value, ObjectId):
				obj_dict[key] = str(value)
			if isinstance(value, list):
				obj_dict[key] = [str(_id) for _id in value]

		return obj_dict
	else:
		raise abort(400, "'obj' type should be 'mongoengine.Document'")


def exception_decorator(errors=(Exception, )):

    def decorator(func):

        def new_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except errors as e:
                return {"err": str(e)}, 400

        return new_func

    return decorator
