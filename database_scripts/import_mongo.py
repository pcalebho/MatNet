from pymongo.mongo_client import MongoClient
import yaml
from pprint import pprint
from bson.objectid import ObjectId

MONGODB_URI = "mongodb+srv://pcalebho:UISBvUYTesMft5AX@matcluster.5ygnbeg.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGODB_URI)

file = "C:/Users/ttrol/CodingProjects/MatNet/webscraper/results_files/AISI_steels_fakedata.yaml"

with open(file, 'r') as f:
    raw_datasheets = yaml.safe_load(f)


material_db = client.material
test_collection = material_db.test_collection

material_id = test_collection.insert_many(raw_datasheets)
pprint(material_id.inserted_ids)
