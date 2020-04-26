from hashlib import md5, sha256
from flask import abort


def custom_hash(string):
	sha256_encoded = sha256((string).encode('utf-8')).hexdigest()
	md5_encoded = md5((sha256_encoded).encode('utf-8')).hexdigest()
	return md5_encoded


def abort_if_invalid_request_params(_dict, attrs):
	for attr in attrs:
		if attr not in _dict:
			abort(400, message=f"Request must contain '{attr}'")
