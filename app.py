from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
boostrap = Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sql'
# Database can add new data after request
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  
db = SQLAlchemy(app)

class Materials(db.Model):
    pass

class Vendors(db.Model):
    pass

class HeatTreatment(db.Model):
    pass

#view function for base page
@app.route('/')
def root():
    return render_template('bootstrap_test.html', name = 'Caleb')
