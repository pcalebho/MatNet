import os
import pandas as pd
from pymongo.mongo_client import MongoClient
from flask import Flask, render_template, request, session, jsonify
from ranking_algo.ranker import rank_materials, get_id

#Connecting and creating MongoDB client instance
MONGODB_URI = "mongodb+srv://pcalebho:UISBvUYTesMft5AX@matcluster.5ygnbeg.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGODB_URI)


material_db = client.material
datasheets_collection = material_db.test_collection

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'


# material_properties = ["Elastic Modulus",
#                        "Yield Strength", "Cost", "Ultimate Strength", "Machineability"]
material_properties = ["Elastic Modulus", "Yield Strength"]
num_sliders = len(material_properties)

def get_form():
    form_data = {}
    for i in range(num_sliders):
        property = get_id(material_properties[i])
        importance = int(request.form[f'sliderRange-{i}'])
        objective = request.form[f'objective-{i}']
        min_value = request.form[f'minValue-{i}']
        max_value = request.form[f'maxValue-{i}']

        if min_value == "":
            min_value = None
        else:
            min_value = int(min_value)

        if max_value == "":
            max_value = None
        else:
            max_value = int(max_value)

        if max_value is not None and min_value is not None and min_value > max_value:
            min_value = None
            max_value = None

        form_data[property] = {
            'importance': importance, 
            'objective': objective, 
            'min': min_value, 
            'max': max_value
        }

    print(form_data)
    
    return form_data
    

@app.route('/', methods = ('GET','POST'))
def root():
    if request.method == 'POST':
        session['form_data'] = get_form()
        # session['form_data'] = request.json
        print(session['form_data'])
        # return jsonify(session['form_data'])
        
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


@app.route('/api/data')
def data():
    form_data = session.get('form_data', [])
    weights = []
    query = []
    if form_data != []:
        for key in form_data:
            if form_data[key]['objective'] == 'minimize':
                weight = form_data[key]['importance']*-1
            else: 
                weight = form_data[key]['importance']
            weights.append(weight)

            if form_data[key]['min'] is None:
                min_value = -1000000
            else:
                min_value = form_data[key]['min']

            if form_data[key]['max'] is None:
                max_value = 1000000
            else:
                max_value = form_data[key]['max']

            query_item = {key: {"$gte": min_value, "$lte": max_value}}
            query.append(query_item)

    if form_data != []:
        cursor = datasheets_collection.find({"$and": query})
    else:
        cursor = datasheets_collection.find()

    materials = []
    for material in cursor:
        material.pop('_id')
        material.pop('link')
        materials.append(material)
    

    if form_data != []:
        result_df = rank_materials(material_properties, weights, materials)
    else:
        result_df = pd.DataFrame(materials)
    

    # search filter
    search = request.args.get('search')

    # sorting
    sort = request.args.get('sort')
    sort_query = {}
    if sort:
        for s in sort.split(','):
            sort_direction = -1 if s[0] == '-' else 1
            sort_name = s[1:]
            if sort_name not in ['elastic_mod','yield_strength','ult_strength','cost','machineability']:
                sort_name = 'elastic_mod'
            sort_query[sort_name] = sort_direction

    # pagination
    start = request.args.get('start', type=int, default=0)
    length = request.args.get('length', type=int, default=0)

    # Perform the query with sorting, skip, and limit parameters
    if search is not None:
        result_df = result_df[result_df.name.str.match(search)]


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

