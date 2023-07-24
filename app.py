import os
import re
import pandas as pd
from pymongo.mongo_client import MongoClient
from flask import Flask, render_template, request, session
from ranking_algo.ranker import rank_materials
import numpy as np

#Connecting and creating MongoDB client instance
MONGODB_URI = "mongodb+srv://pcalebho:UISBvUYTesMft5AX@matcluster.5ygnbeg.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGODB_URI)


material_db = client.material
datasheets_collection = material_db.test_collection

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

num_sliders = 5
material_properties = ["", "Elastic Modulus",
                       "Yield Strength", "Cost", "Ultimate Strength", "Machineability"]


@app.route('/', methods = ('GET','POST'))
def root():
    if request.method == 'POST':
        criterions = [request.form[f'Criterion-{i}'] for i in range(num_sliders)]
        weights = [request.form[f'sliderRange-{i}'] for i in range(num_sliders)]
        
        session['criterions'] = criterions
        session['weights'] = weights

    
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
    # Retrieve the criterions and weights from the session
    criterions = session.get('criterions', [])
    weights = session.get('weights', [])
    weights = [int(i) for i in weights]

    materials = []
    for material in datasheets_collection.find():
        material.pop('_id')
        material.pop('link')
        materials.append(material)
    
    if criterions != [] and weights != []:
        result_df = rank_materials(criterions, weights, materials)
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

    total = result_df.shape[0]


    # Check if start and length are not None and use the default values if necessary
    if start is None:
        start = 0
    if length is None:
        length = 0

    # Sorting the query_result based on the 'sort_query' dictionary
    if sort_query: 
        if sort_direction < 0:
            ascend = True
        else:
            ascend = False

        result_df = result_df.sort_values(by=sort_name, ascending = ascend)


    # Applying skip and limit after sorting
    if start >= 0 and length >= 0:
        result_df = result_df.iloc[start:(start+length)]

    return {
                'data': result_df.to_dict('records'),
                'total': total
            }

