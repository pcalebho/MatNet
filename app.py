from flask import Flask, render_template
# from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# boostrap = Bootstrap(app)
db = SQLAlchemy()

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# Database can add new data after request
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  

db.init_app(app)

#This model is used to create a table and add rows
class Materials(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    material_name = db.Column(db.String, unique=True, nullable=False)
    ultimate_strength = db.Column(db.Integer)
    yield_strength = db.Column(db.Integer)
    

    #Method used for outputting String representation 
    def __repr__(self):
        return '<Material Name: %r>' % self.material_name

# class Vendors(db.Model):
#     pass

# class HeatTreatment(db.Model):
#     pass

#view function for base page
@app.route('/')
def root():
    return render_template('index.html')

#view function for contact slide
@app.route('/contact')
def contact():
    return '<h2> Contact me at pcalebho@gmail.com </h2>'
