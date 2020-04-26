from mongoengine import Document, StringField, EmailField, ReferenceField, DateTimeField, URLField, ListField


class User(Document):
	first_name = StringField(required=True)
	last_name = StringField(required=True)
	email = EmailField(required=True, unique=True)
	phone = StringField(required=True, unique=True)
	password = StringField(required=True)

	def __repr__(self):
		return self.first_name + ' ' + self.last_name


class Experience(Document):
	user = ReferenceField(User, required=True)
	position = StringField(required=True)
	organization = StringField(required=True)
	job_category = ReferenceField('JobCategory', required=True)
	date_start = DateTimeField(required=True)
	date_end = DateTimeField(required=True)
	country = StringField(required=True)


class Education(Document):
	user = ReferenceField(User, required=True)
	degree = StringField(required=True)
	organization = StringField(required=True)
	date_start = DateTimeField(required=True)
	date_end = DateTimeField(required=True)
	country = StringField(required=True)


class Certificate(Document):
	user = ReferenceField(User, required=True)
	title = StringField(required=True)
	description = StringField(required=True)
	url = URLField(required=True)


class Medcard(Document):
	user = ReferenceField(User, required=True)
	title = StringField(required=True)
	url = URLField(required=True)


class Resume(Document):
	user = ReferenceField(User, required=True)
	experiences = ListField(ReferenceField(Experience))
	educations = ListField(ReferenceField(Education))
	medcards = ListField(ReferenceField(Medcard))
	certificates = ListField(ReferenceField(Certificate))
	summary = StringField()