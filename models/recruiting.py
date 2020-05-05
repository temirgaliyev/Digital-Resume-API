from mongoengine import Document, StringField, EmailField, ReferenceField, IntField, BooleanField


class Organization(Document):
	code = StringField(required=True, unique=True)
	name = StringField(required=True)
	description = StringField()


class Recruiter(Document):
	first_name = StringField(required=True)
	last_name = StringField(required=True)
	email = EmailField(required=True, unique=True)
	phone = StringField(required=True, unique=True)
	password = StringField(required=True)
	organization = StringField(required=True)


class ApplicantEvaluation(Document):
	recruiter = ReferenceField(Recruiter, required=True)
	application = ReferenceField('Application', required=True)
	notes = StringField()
	in_progress = BooleanField(default=True)
	hired = BooleanField(null=True)
