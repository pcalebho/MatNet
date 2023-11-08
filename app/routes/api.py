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


KSI_TO_MPA = 6.89476

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

@api_bp.route('/api/fatigue/<fatigue_id>')
def get_fatigue(fatigue_id):
    fatigue_data = Fatigue.objects(pk=fatigue_id).first()           #type: ignore
    
    raw_curves = fatigue_data.graph
    ksi_to_MPa = 6.89476

    table = pd.DataFrame(raw_curves)
    table = table.iloc[:, :3]
    table[0] = table[0].astype(float)
    table[1] = table[1].astype(float).round(0)
    table[2] = table[2].astype(float).mul(ksi_to_MPa).round(0)
    table.columns = ['curve_label', 'num_cycles', 'max_stress']
    labels = table["curve_label"].unique()
    

    return {
        "description": fatigue_data.description,
        "material_name": fatigue_data.material_name,
        "data": table.to_dict('records'),
        "labels": list(labels),
    }

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

                    if 'importance' in filter['value']:
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
                    field = filter["field"]
                    if field == "name":
                        field = "material_name"
                    regex_search = f'{filter["value"]}'
                    minMaxQuery.append({field: {"$regex": regex_search}})
                else:
                    scale_factor = KSI_TO_MPA
                    if filter['field'] == 'k_value':
                        scale_factor = 1
                    if filter['value']['start'] != '':
                        field = filter['field']
                        if field == "tensile_strength_yield":
                            field = "tys_ksi_min"
                        if field == "tensile_strength_ultimate":
                            field = "tus_ksi_min"
                        minMaxQuery.append({field :{'$gte' : float(filter['value']['start'])/scale_factor}})  #type: ignore
                    if filter['value']['end'] != '':
                        field = filter['field']
                        if field == "tensile_strength_yield":
                            field = "tys_ksi_max"
                        if field == "tensile_strength_ultimate":
                            field = "tus_ksi_max"
                        minMaxQuery.append({field :{'$lte' : float(filter['value']['end'])/scale_factor}})    #type: ignore

        print(minMaxQuery)

        if minMaxQuery == [] and fatigue_collection is not None:
            cursor = fatigue_collection.find()
        else:
            cursor = fatigue_collection.find({"$and": minMaxQuery})              #type: ignore

        materials = []
        for material in cursor:
            flattened_material = {}
            flattened_material['name'] = material['material_name']
            flattened_material['tensile_strength_ultimate'] =  _convert_units(material['tus_ksi'])
            flattened_material['tensile_strength_yield'] =  _convert_units(material['tys_ksi'])
            flattened_material['k_value'] = material['k_value']
            flattened_material['product_form'] = material['product_form']
            flattened_material['id'] = str(material['_id'])
            flattened_material['link_label'] = 'See detailed curve'
            materials.append(flattened_material)
        

        result_df = pd.DataFrame(materials)
        result_df = result_df.sample(frac=1).reset_index(drop=True)


        return {
                    'data': result_df.to_dict('records'),
                }

def _convert_units(text):
    """
    Convert string from ksi to MPa
    """
    if text is None or text == "":
        return
    
    string_list = text.split('-')
    if len(string_list) == 1:
        string_list = text.split(', ')
    float_list = [round(float(i)*KSI_TO_MPA) for i in string_list]

    if len(float_list) == 1:
        return str(float_list[0])
    elif len(float_list) == 2:
        return str(float_list[0])+' - '+str(float_list[1])