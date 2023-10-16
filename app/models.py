from flask_login import UserMixin 
from mongoengine import Document, StringField

class User(Document, UserMixin):
    email = StringField(required=True)
    password = StringField(required=True)
    industry = StringField(max_length=50)
    occupation = StringField(max_length=50)

