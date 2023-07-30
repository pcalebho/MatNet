import os
import pandas as pd
from pymongo.mongo_client import MongoClient
from flask import Flask, render_template, request, session, jsonify
from ranking_algo.ranker import rank_materials, get_id

#Connecting and creating MongoDB client instance
# MONGODB_URI = "mongodb+srv://pcalebho:UISBvUYTesMft5AX@matcluster.5ygnbeg.mongodb.net/?retryWrites=true&w=majority"
#For testing
MONGODB_URI = 'mongodb://localhost:27017' 
client = MongoClient(MONGODB_URI)


material_db = client.matjet
datasheets_collection = material_db.materials

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'


# material_properties = ["Elastic Modulus",
#                        "Yield Strength", "Cost", "Ultimate Strength", "Machineability"]
material_properties = ["Density", "Yield Strength"]
num_sliders = len(material_properties)
    

@app.route('/')
def root(): 
    session.clear()     
    return render_template(
        'index.html', 
        material_properties=material_properties,
        matprop_len=len(material_properties), 
        num_sliders=num_sliders
    )

# view function for contact slide
@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/documentation')
def glossary():
    return render_template('glossary.html')


@app.route('/api/data', methods = ('GET','POST'))
def data():
    if request.method == 'POST':
        query = []
        weights = []
        
        form_data = request.json
        if form_data is not None:
            for key in form_data:
                if form_data[key]['objective'] == 'minimize':
                    weight = form_data[key]['importance']*-1
                else: 
                    weight = form_data[key]['importance']
                weights.append(weight)

                if form_data[key]['min'] == "":
                    min_value = -1000000
                else:
                    min_value = int(form_data[key]['min'])

                if form_data[key]['max'] == "":
                    max_value = 1000000
                else:
                    max_value = int(form_data[key]['max'])

                query_item = {get_id(key): {"$gte": min_value, "$lte": max_value}}      #type: ignore
                query.append(query_item)
        session['query'] = query
        session['form_data'] = form_data
        session['weights'] = weights
            
        return jsonify(form_data, weights, query)
    else:
        form_data = session.get('form_data', {})
        query = session.get('query',{})
        weights = session.get('weights',[])
        print('WEIGHTS: ', weights)
        print('FORM: ', form_data)
        print('QUERY: ', query)

    
    if query != {}:
        cursor = datasheets_collection.find({"$and": query})
    else:
        cursor = datasheets_collection.find()

    materials = []
    for material in cursor:
        flattened_material = {}
        flattened_material['name'] = material['name']
        flattened_material.update(material['physical_properties'])
        flattened_material.update(material['mechanical_properties'])
        materials.append(flattened_material)
    

    if form_data != {}:
        result_df = rank_materials(material_properties, weights, materials)
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
            if sort_name not in ['modulus_of_elasticity','tensile_strength_yield','tensile_strength_ultimate','machinability']:
                sort_name = 'modulus_of_elasticity'
            sort_query[sort_name] = sort_direction

    # pagination
    start = request.args.get('start', type=int, default=0)
    length = request.args.get('length', type=int, default=0)

    # Perform the query with sorting, skip, and limit parameters
    if search is not None:
        result_df = result_df[result_df.name.str.contains(search)]


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

