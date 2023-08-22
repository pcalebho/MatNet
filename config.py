import os
from dotenv import load_dotenv

load_dotenv()

def check_none(str):
    if str is None:
        raise TypeError('Wrong Type')

class Config():
    #Custom config values
    MONGODB_URI = os.environ.get('MONGODB_URI')
    MATERIAL_DB_NAME = os.environ.get('DATABASE')
    MATERIAL_COLLECTION = os.environ.get('MATERIAL_COLLECTION')
    POSTGRESQL_URI= os.environ.get('POSTGRESQL_URI')
    
    
    #Built-in Flask config values
    SQLALCHEMY_DATABASE_URI = POSTGRESQL_URI
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}  #Needed to stop the SQL disconnect issues
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = False

class DevConfig(Config):
    DEBUG = True

class ProdConfig(Config):
    DEBUG = False