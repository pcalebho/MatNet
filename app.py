import os
import re
from pymongo.mongo_client import MongoClient
from flask import Flask, render_template, request

#Connecting and creating MongoDB client instance
MONGODB_URI = "mongodb+srv://pcalebho:UISBvUYTesMft5AX@matcluster.5ygnbeg.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGODB_URI)


material_db = client.material
datasheets_collection = material_db.test_collection

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)


num_sliders = 5
material_properties = ["", "Elastic Modulus",
                       "Yield Strength", "Desnity", "Cost", "Ultimate Strength", "Machineability"]


@app.route('/', methods = ('GET','POST'))
def root():
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
    query = {}

    # search filter
    search = request.args.get('search')
    if search:
        query = {'name': {'$regex': re.escape(search), '$options': 'i'}}

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
    query_result = datasheets_collection.find(query)

    # Check if start and length are not None and use the default values if necessary
    if start is None:
        start = 0
    if length is None:
        length = 0

    # Sorting the query_result based on the 'sort_query' dictionary
    if sort_query:
        query_result = query_result.sort(list(sort_query.items()))

    # Applying skip and limit after sorting
    if start >= 0 and length >= 0:
        query_result = query_result.skip(start).limit(length)

    materials = []
    for material in query_result:
        material.pop('_id')
        material.pop('link')
        materials.append(material)

    total = datasheets_collection.count_documents(query)

    # response
    return {
        'data': materials,
        'total': total,
    }
