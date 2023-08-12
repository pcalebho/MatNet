import os
import pandas as pd

from flask_login import LoginManager
from routes.api import api_bp
from routes.docs import docs_bp
from pymongo.mongo_client import MongoClient
from flask import Flask, render_template, request, session, jsonify, redirect, flash, url_for
from ranking_algo.ranker import rank_materials, get_key, CRITERION_KEY, KEY
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError


load_dotenv()

app = Flask(__name__)

#get and use environment variables
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('POSTGRESQL_URI')


#Connect to Postgresql database
user_db = SQLAlchemy()
user_db.init_app(app)


#SQL Model for User
class User(user_db.Model):
    id = user_db.Column(user_db.Integer, primary_key=True)
    email = user_db.Column(user_db.String(80), unique=True, nullable=False)
    password = user_db.Column(user_db.Text(), nullable=False)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

# login_manager = LoginManager()
# login_manager.init_app(app)

bcrypt = Bcrypt(app)

#registration form
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(form, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already in use.')

#login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


with app.app_context():
    user_db.create_all()


material_properties = list(KEY.keys())
num_sliders = len(material_properties)

#register blueprints
app.register_blueprint(api_bp)
app.register_blueprint(docs_bp)

#Home
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


@app.route('/healthcheck')
def health_check():
    return "Success", 200

@app.route('/login')
def login():
    return render_template('login.html', title='Login')

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_email = form.email.data
        new_user = User(email=user_email, password=pw_hash)
        user_db.session.add(new_user)
        user_db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect('/')

    return render_template('register.html', title='Register', form=form)


