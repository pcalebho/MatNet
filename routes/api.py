import os
import pandas as pd

from dotenv import load_dotenv
from pymongo import MongoClient
from flask import Blueprint, request, session, jsonify
from ranking_algo.ranker import get_key, CRITERION_KEY, rank_materials

load_dotenv()

MONGODB_URI = os.environ.get('MONGODB_URI')
db_name = os.environ.get('DATABASE')
collection_name = os.environ.get('MATERIAL_COLLECTION')

if db_name is None or collection_name is None:
    raise ValueError('Error: DATABASE ENV var is missing')

if collection_name is None:
    raise ValueError('Error: MATERIAL_COLLECTION ENV var is missing')

#Connecting and creating MongoDB client instance
client = MongoClient(MONGODB_URI)
material_db = client[db_name]
datasheets_collection = material_db[collection_name]

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/api/data', methods = ('GET','POST'))
def data():
    if request.method == 'POST':
        query = []
        
        form_data = request.json
        if form_data is not None:
            for key in form_data:
                if form_data[key]['min'] == "":
                    form_data[key]['min'] = -1000000
                else:
                    form_data[key]['min'] = int(form_data[key]['min'])

                if form_data[key]['max'] == "":
                     form_data[key]['max'] = 1000000
                else:
                     form_data[key]['max'] = int(form_data[key]['max'])

                query_item = {
                    get_key(key): {
                        "$gte": form_data[key]['min'], 
                        "$lte": form_data[key]['max']
                    }
                }      #type: ignore
                query.append(query_item)
            query.append({"mechanical_properties.hardness_brinell.units": ''})
        
        session['query'] = query
        session['form_data'] = form_data
            
        return jsonify({'form_data': form_data, 'query': query})
    else:
        form_data = session.get('form_data', {})
        query = session.get('query',[])
        

    valid_query = {"$and": [
        {"mechanical_properties.hardness_brinell.units": ''},
        {"mechanical_properties.hardness_brinell.value":{'$exists': True}},
        {"mechanical_properties.machinability.value": {'$exists': True}},
        {"physical_properties.density.value": {'$exists': True}},
        {"thermal_properties.specific_heat_capacity.value": {'$exists': True}},
        {"mechanical_properties.tensile_strength_yield.value": {"$exists": True}},
        {"mechanical_properties.tensile_strength_ultimate.value": {"$exists": True}},
        {"mechanical_properties.modulus_of_elasticity.value": {"$exists": True}}
    ]}
    
    if 'query' in session:
        cursor = datasheets_collection.find({"$and": query})
    else:
        cursor = datasheets_collection.find(valid_query)
    

    materials = []
    for material in cursor:
        flattened_material = {}
        flattened_material['name'] = material['name']
        flattened_material['cost'] = material['cost']['value']
        flattened_material['density'] =  material['physical_properties']['density']['value']
        flattened_material['tensile_strength_ultimate'] =  material['mechanical_properties']['tensile_strength_ultimate']['value']
        flattened_material['tensile_strength_yield'] =  material['mechanical_properties']['tensile_strength_yield']['value']
        flattened_material['modulus_of_elasticity'] = material['mechanical_properties']['modulus_of_elasticity']['value']
        flattened_material['specific_heat_capacity'] = material['thermal_properties']['specific_heat_capacity']['value']
        flattened_material['machinability'] = material['mechanical_properties']['machinability']['value']
        flattened_material['hardness_brinell'] = material['mechanical_properties']['hardness_brinell']['value']
        materials.append(flattened_material)
    

    if form_data != {}:
        result_df = rank_materials(form_data, materials)
    else:
        result_df = pd.DataFrame(materials)

    result_df = result_df.fillna('N/A')

    # search filter
    search = request.args.get('search')

    # sorting
    sort = request.args.get('sort')
    sort_query = {}
    if sort:
        for s in sort.split(','):
            sort_direction = -1 if s[0] == '-' else 1
            sort_name = s[1:]
            if sort_name not in list(CRITERION_KEY.values()):
                sort_name = 'name'
            sort_query[sort_name] = sort_direction

    # pagination
    start = request.args.get('start', type=int, default=0)
    length = request.args.get('length', type=int, default=0)

    # Perform the query with sorting, skip, and limit parameters
    if search is not None:
        search = search.lower()
        result_df = result_df[result_df.name.str.contains(search, case=False)]


    # Check if start and length are not None and use the default values if necessary
    if start is None:
        start = 0
    if length is None:
        length = 0

    # Sorting the query_result based on the 'sort_query' dictionary
    if sort_query: 
        if sort_direction < 0:      #type: ignore
            ascend = True
        else:
            ascend = False

        result_df = result_df.sort_values(by=sort_name, ascending = ascend)     #type: ignore

    total = result_df.shape[0]

    # Applying skip and limit after sorting
    if start >= 0 and length >= 0:
        result_df = result_df.iloc[start:(start+length)]

    return {
                'data': result_df.to_dict('records'),
                'total': total
            }