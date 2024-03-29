import os
from dotenv import load_dotenv

load_dotenv()

def check_none(str):
    if str is None:
        raise TypeError('Wrong Type')

class Config():
    #Custom config values
    MONGODB_URI = os.environ.get('MONGODB_URI')
    MONGODB_HOST = os.environ.get('MONGODB_HOST')
    MONGODB_USERNAME = os.environ.get('MONGODB_USERNAME')
    MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD')
    MATERIAL_DB_NAME = os.environ.get('DATABASE')
    MATERIAL_COLLECTION = os.environ.get('MATERIAL_COLLECTION')
    USER_COLLECTION = os.environ.get('USER_COLLECTION')
    FATIGUE_COLLECTION = os.environ.get('FATIGUE_COLLECTION')
    POSTGRESQL_URI= os.environ.get('POSTGRESQL_URI')

    MONGODB_SETTINGS = [{
        "db": MATERIAL_DB_NAME,
        "host": MONGODB_HOST,
        "username": MONGODB_USERNAME,
        "password": MONGODB_PASSWORD
    }]
    
    #Built-in Flask config value
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = False

class DevConfig(Config):
    DEBUG = True
    MATERIAL_DB_NAME = os.environ.get('DEV_DATABASE')

class ProdConfig(Config):
    DEBUG = False