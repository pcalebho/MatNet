from flask_login import UserMixin 
from mongoengine import Document, StringField, EmailField

class User(Document, UserMixin):
    email = EmailField(required=True, unique= True)
    password = StringField(required=True)
    industry = StringField(max_length=50)
    occupation = StringField(max_length=50)

