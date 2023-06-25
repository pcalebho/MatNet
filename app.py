import os

from flask import Flask, render_template
# from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
db = SQLAlchemy()

# app.config['SQLALCHEMY_DATABASE_URI'] = \
#     'sqlite:///' + os.path.join(basedir, 'data.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:JetMat_22@localhost/testdb'
# Database can add new data after request
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db.init_app(app)


num_sliders = 5
material_properties = ["", "Elastic Modulus",
                       "Yield Strength", "Weight", "Cost", "4a", "six"]

# This model is used to create a table and add rows


class Materials(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    material_name = db.Column(db.String, unique=True, nullable=False)
    ultimate_strength = db.Column(db.Integer)
    yield_strength = db.Column(db.Integer)

    # Method used for outputting String representation

    def __repr__(self):
        return '<Material Name: %r>' % self.material_name


with app.app_context():
    db.create_all()
# class Vendors(db.Model):
#     pass

# class HeatTreatment(db.Model):
#     pass

# view function for base page


@app.route('/')
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
