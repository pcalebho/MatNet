import os
from pymongo.mongo_client import MongoClient
from flask import Flask, render_template

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
    datasheets = datasheets_collection.find()

    return render_template(
        'index.html', 
        material_properties=material_properties,
        matprop_len=len(material_properties), 
        num_sliders=num_sliders,
        datasheets=datasheets
    )

# view function for contact slide


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/documentation')
def glossary():
    return render_template('glossary.html')
