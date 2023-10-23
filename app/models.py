from flask_login import UserMixin 
from mongoengine import Document, StringField, EmailField, DictField, ListField
class User(Document, UserMixin):
    email = EmailField(required=True, unique= True)
    password = StringField(required=True)
    industry = StringField(max_length=50)
    occupation = StringField(max_length=50)

    def get_id(self):
        return self.email
    
class Fatigue(Document):
    description = StringField()
    material_name = StringField()
    product_form = StringField()
    k_value = StringField()
    tus = StringField(db_field = 'tus_ksi')
    tys = StringField(db_field = 'tys_ksi')
    temp = StringField(db_field='temp_F')
    equations = DictField(db_field='equivalent_stress_equations')
    graph = ListField()

    meta = {'collection': 'fatigue_data'}