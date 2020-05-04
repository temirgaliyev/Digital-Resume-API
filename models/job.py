from datetime import datetime
from mongoengine import Document, StringField, DateTimeField, ReferenceField, IntField, BooleanField


class JobCategory(Document):
	code = StringField(required=True, unique=True)
	name = StringField(required=True, unique=True)
	description = StringField(required=True)


class Job(Document):
	code = StringField(required=True)
	name = StringField(required=True)
	description = StringField(required=True)
	date_published = DateTimeField(default=datetime.utcnow)
	job_category = ReferenceField(JobCategory, required=True)
	recruiter = ReferenceField('Recruiter', required=True)
	organization = ReferenceField('Organization', required=True)
	position = StringField(required=True)
	salary_min = IntField()
	salary_max = IntField()
	currency = StringField(default='kzt', choices=('kzt', 'usd', 'rub'))
	is_available = BooleanField(default=True)
