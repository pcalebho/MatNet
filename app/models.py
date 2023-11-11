from flask_login import UserMixin 
from mongoengine import Document, StringField, EmailField, DictField, ListField, FloatField, BooleanField
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
    k_value = FloatField()
    tus = StringField(db_field = 'tus_ksi')
    tys = StringField(db_field = 'tys_ksi')
    tus_max = FloatField(db_field = 'tus_ksi_max') 
    tus_min = FloatField(db_field = 'tus_ksi_min') 
    tys_max = FloatField(db_field = 'tys_ksi_max') 
    tys_min = FloatField(db_field = 'tys_ksi_min') 
    temp = StringField(db_field='temp_F')
    equations = DictField(db_field='equivalent_stress_equations')
    graph = ListField()
    source = StringField()
    category = StringField()

    meta = {'collection': 'fatigue_data'}

class Inquiries(Document):
    email = StringField(required=True)
    type = StringField(required=True)
    subject = StringField(required=True)
    message = StringField(required=True)
    addressed = BooleanField(required=True, default=False)