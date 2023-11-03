from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URI = os.environ.get('MONGODB_URI')


client = MongoClient(MONGODB_URI)

material_db = client[os.environ.get('DEV_DATABASE')]        #type:ignore
fatigue_collection = material_db[os.environ.get('FATIGUE_COLLECTION')]      #type:ignore

for mat in fatigue_collection.find():
    raw_tus = mat['tus_ksi'] 
    raw_tys = mat['tys_ksi']

    if raw_tys is None:
        split_tys = [0]
    else:
        split_tys = raw_tys.split('-')
        if len(split_tys) < 2:
            split_tys = split_tys[0].split(', ')

    if raw_tus is None:
        split_tus = [0]
    else:
        split_tus = raw_tus.split('-')
        if len(split_tus) < 2:
            split_tus = split_tus[0].split(', ')

    new_fields = {}
    new_fields['tus_ksi_max'] = float(split_tus[-1])
    new_fields['tus_ksi_min'] = float(split_tus[0])
    new_fields['tys_ksi_max'] = float(split_tys[-1])
    new_fields['tys_ksi_min'] = float(split_tys[0])
    try:
        new_fields['k_value'] = float(mat['k_value'])
    except Exception:
        print(mat['_id'])


    fatigue_collection.update_one({'_id': mat['_id']}, {'$set': new_fields} )
    

    
