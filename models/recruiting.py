from mongoengine import Document, StringField, EmailField, ReferenceField, IntField, BooleanField


class Organization(Document):
	code = StringField(required=True)
	name = StringField(required=True)
	description = StringField(required=True)


class Recruiter(Document):
	first_name = StringField(required=True)
	last_name = StringField(required=True)
	email = EmailField(required=True, unique=True)
	phone = StringField(required=True, unique=True)
	organization = StringField(required=True)


class ApplicantEvaluation(Document):
	notes = StringField()
	recruiter = ReferenceField(Recruiter, required=True)
	application = ReferenceField('Application', required=True)
	in_progress = BooleanField(default=True)
	hired = BooleanField(null=True)
