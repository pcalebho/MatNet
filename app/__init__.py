''''
factory function to create the app
'''

import os

from flask import Flask, render_template
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()

def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config=False)

    if test_config is None:
        app.config.from_object('config.Config')
    elif test_config == 'development':
        app.config.from_object('config.DevConfig')
    elif test_config == 'production':
        app.config.from_object('config.ProdConfig')
    else:
        raise ValueError('No corresponding arg value')


    #initialize db extensions and models
    from app.models import db, User
    db.init_app(app)
    migrate = Migrate(app, db)

    #login logic
    login_manager = LoginManager()    
    login_manager.init_app(app)

    #callback function for the login manager
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))


    with app.app_context():
        #create tables if they have not already been made
        db.create_all()

        #register blueprints
        from .routes.api import api_bp
        from .routes.docs import docs_bp
        from .routes.main import main_bp
        from .routes.auth import auth_bp
        app.register_blueprint(main_bp)
        app.register_blueprint(api_bp)
        app.register_blueprint(docs_bp)
        app.register_blueprint(auth_bp)
        

        #other view functions
        @app.route('/healthcheck')
        def health_check():
            return "Success", 200

        # view function for contact slide
        @app.route('/contact')
        def contact():
            return render_template('contact.html')
    
        return app
