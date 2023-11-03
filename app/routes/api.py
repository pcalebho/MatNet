import os
import pandas as pd
import json

from dotenv import load_dotenv
from pymongo import MongoClient
from flask import Blueprint, request, session, jsonify, current_app
from app.ranker import get_key, CRITERION_KEY, rank_materials
from flask_login import current_user, login_required
from app.models import Fatigue

load_dotenv()

MONGODB_URI = current_app.config['MONGODB_URI']
db_name = current_app.config['MATERIAL_DB_NAME']
collection_name = current_app.config['MATERIAL_COLLECTION']
fatigue_collection_name = current_app.config['FATIGUE_COLLECTION']

#Connecting and creating MongoDB client instance
try:
    client = MongoClient(MONGODB_URI)
    material_db = client[db_name]
    datasheets_collection = material_db[collection_name]
    fatigue_collection = material_db[fatigue_collection_name]
except Exception:
    datasheets_collection = None
    fatigue_collection = None
    print('Error: ', 'api endpoint mongodb error connection')

api_bp = Blueprint('api', __name__)

current_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the JSON file
file_path = os.path.join(current_directory, '..', 'static', 'sampleData.json')

# Using the 'with' statement to open and automatically close the file
with open(file_path, 'r') as json_file:
    sample_data = json.load(json_file)

@api_bp.route('/api/sample')
def sample():
    return jsonify({'data': sample_data})

@api_bp.route('/api/tabulator/params/<params>')
def get_data(params):
    form_data = {}
    search_term = ""

    param_dict = json.loads(params)
    filters = param_dict['filter']
    source = param_dict['source']

    if source == 'general':
        minMaxQuery = [
            {"mechanical_properties.hardness_brinell.units": ''},
            {"mechanical_properties.hardness_brinell.value":{'$exists': True}},
            {"mechanical_properties.machinability.value": {'$exists': True}},
            {"physical_properties.density.value": {'$exists': True}},
            {"thermal_properties.specific_heat_capacity.value": {'$exists': True}},
            {"mechanical_properties.tensile_strength_yield.value": {"$exists": True}},
            {"mechanical_properties.tensile_strength_ultimate.value": {"$exists": True}},
            {"mechanical_properties.modulus_of_elasticity.value": {"$exists": True}}
        ]

        if filters != []:
            for filter in filters:
                if filter["type"] == "like":
                    search_term = filter["value"]
                else:
                    query = {
                        get_key(filter["field"]): {
                            '$gte': -10000000,
                            '$lte': 10000000
                        }
                    }
                    if filter['value']['start'] != '':
                        query[get_key(filter['field'])]['$gte'] = float(filter['value']['start'])  #type: ignore
                    if filter['value']['end'] != '':
                        query[get_key(filter['field'])]['$lte'] = float(filter['value']['end'])    #type: ignore
                    minMaxQuery.append(query)

                    if int(filter['value']['importance']) != 0 or 'importance' in filter['value']:
                        form_data[filter['field']] = {'importance': int(filter['value']['importance']),'objective': 'min' if filter['value']['objective'] else 'max'}
        
        cursor = datasheets_collection.find({"$and": minMaxQuery})              #type: ignore

        materials = []
        for material in cursor:
            flattened_material = {}
            flattened_material['name'] = material['name']
            flattened_material['density'] =  material['physical_properties']['density']['value']
            flattened_material['tensile_strength_ultimate'] =  material['mechanical_properties']['tensile_strength_ultimate']['value']
            flattened_material['tensile_strength_yield'] =  material['mechanical_properties']['tensile_strength_yield']['value']
            flattened_material['modulus_of_elasticity'] = material['mechanical_properties']['modulus_of_elasticity']['value']
            flattened_material['cost'] = material['cost']['value']
            flattened_material['specific_heat_capacity'] = material['thermal_properties']['specific_heat_capacity']['value']    
            flattened_material['machinability'] = material['mechanical_properties']['machinability']['value']
            flattened_material['hardness_brinell'] = material['mechanical_properties']['hardness_brinell']['value']
            flattened_material['categories'] = material['categories']
            flattened_material['component_elements_properties'] = material['component_elements_properties']
            materials.append(flattened_material)
        

        result_df = pd.DataFrame(materials)
        result_df = result_df.sample(frac=1).reset_index(drop=True)

        if form_data != {}:
            result_df = rank_materials(form_data, result_df)  

        if search_term != "":
            result_df = result_df[result_df['name'].str.contains(search_term, case=False)]


        return {
                    'data': result_df.to_dict('records'),
                }
    else:
        minMaxQuery = []

        if filters != []:
            for filter in filters:
                if filter["type"] == "like":
                    search_term = filter["value"]
                else:
                    query = {
                        get_key(filter["field"]): {
                            '$gte': -10000000,
                            '$lte': 10000000
                        }
                    }
                    if filter['value']['start'] != '':
                        query[get_key(filter['field'])]['$gte'] = float(filter['value']['start'])  #type: ignore
                    if filter['value']['end'] != '':
                        query[get_key(filter['field'])]['$lte'] = float(filter['value']['end'])    #type: ignore
                    minMaxQuery.append(query)

                    if int(filter['value']['importance']) != 0 or 'importance' in filter['value']:
                        form_data[filter['field']] = {'importance': int(filter['value']['importance']),'objective': 'min' if filter['value']['objective'] else 'max'}
        
        if minMaxQuery == [] and fatigue_collection is not None:
            cursor = fatigue_collection.find()
        else:
            cursor = fatigue_collection.find({"$and": minMaxQuery})              #type: ignore

        materials = []
        for material in cursor:
            flattened_material = {}
            flattened_material['name'] = material['material_name']
            flattened_material['density'] = 10
            flattened_material['tensile_strength_ultimate'] =  material['tus_ksi']
            flattened_material['tensile_strength_yield'] =  material['tys_ksi']
            flattened_material['k_value'] = material['k_value']
            flattened_material['product_form'] = material['product_form']
            materials.append(flattened_material)
        

        result_df = pd.DataFrame(materials)
        result_df = result_df.sample(frac=1).reset_index(drop=True)

        if form_data != {}:
            result_df = rank_materials(form_data, result_df)  

        if search_term != "":
            result_df = result_df[result_df['name'].str.contains(search_term, case=False)]


        return {
                    'data': result_df.to_dict('records'),
                }


@api_bp.route('/api/fatigue', methods = ('GET','POST'))
def fatigue_data():
    def ksi_to_mpa(ksi):
        mpa = ksi*6.89476
        return mpa
    
    

    query = Fatigue.objects   # type: ignore

    data = [doc.graph for doc in query]
    return data