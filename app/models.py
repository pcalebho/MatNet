from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    industry = db.Column(db.String(80), nullable=False)
    occupation = db.Column(db.String(20), nullable=False)
