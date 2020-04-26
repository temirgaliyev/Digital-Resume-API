from datetime import datetime
from models import Job, Resume
from mongoengine import Document, DateTimeField, ReferenceField, StringField

class Application(Document):
	date_of_application = DateTimeField(default=datetime.utcnow)
	job = ReferenceField(Job, required=True)
	resume = ReferenceField(Resume, required=True)
	cover_letter = StringField()
