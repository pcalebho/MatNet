import os
from pymongo.mongo_client import MongoClient
from flask import Flask, render_template
# from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

MONGODB_URI = "mongodb+srv://pcalebho:UISBvUYTesMft5AX@matcluster.5ygnbeg.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGODB_URI)

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)


num_sliders = 5
material_properties = ["", "Elastic Modulus",
                       "Yield Strength", "Weight", "Cost", "Ultimate Strength", "six"]


@app.route('/', methods = ('GET','POST'))
def root():
    return render_template('index.html', material_properties=material_properties,
                           matprop_len=len(material_properties), num_sliders=num_sliders)

# view function for contact slide


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/documentation')
def glossary():
    return render_template('glossary.html')
