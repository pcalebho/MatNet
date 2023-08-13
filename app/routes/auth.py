from app.models import User, db
from flask import render_template, current_app, Blueprint, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user, login_required
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

auth_bp = Blueprint('auth', __name__)

bcrypt = Bcrypt(current_app)

class RegistrationForm(FlaskForm):
    occupation_choices = {
        'student': 'Student',
        'design_engineer': 'Design Engineer',
        'civil_engineer': 'Civil Engineer',
        'teacher': 'Teacher',
        'other': 'Other'
    }

    industry_choices = {
        'aerospace/defense': 'Aerospace/Defense',
        'hvac': 'HVAC',
        'maritime': 'Maritime'
    }

    email = StringField('Email', validators=[DataRequired(), Email()])
    industry = SelectField('What industry are you in?', choices=industry_choices.items(),validators=[DataRequired()])
    occupation = SelectField('What is your occupation?', choices=occupation_choices.items(),validators=[DataRequired()])
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

    

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()

            # check if user actually exists
            # take the user supplied password, hash it, and compare it to the hashed password in database
            if not user or not bcrypt.check_password_hash(user.password, form.password.data): 
                flash('Please check your login details and try again.')
                return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

            # if the above check passes, then we know the user has the right credentials
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.root'))
        else:
            print(form.errors)

    return render_template('login.html', title='Login', form=form)


@auth_bp.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_email = form.email.data
        user_industry = form.industry.data
        user_occupation = form.occupation.data
        new_user = User(email=user_email, password=pw_hash, industry=user_industry, occupation=user_occupation)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect('/')

    return render_template('register.html', title='Register', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.root'))