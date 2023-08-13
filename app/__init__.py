''''
factory function to create the app
'''

import os

from flask import Flask, render_template
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'development'
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('POSTGRESQL_URI')


    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    
    from app.models import db
    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        #create tables if they have not already been made
        db.create_all()

        from .routes.api import api_bp
        from .routes.docs import docs_bp
        from .routes.main import main_bp
        from .routes.auth import auth_bp
        app.register_blueprint(main_bp)
        app.register_blueprint(api_bp)
        app.register_blueprint(docs_bp)
        app.register_blueprint(auth_bp)
        
        # from routes.main import main_bp

        #other view functions
        @app.route('/healthcheck')
        def health_check():
            return "Success", 200

        # view function for contact slide
        @app.route('/contact')
        def contact():
            return render_template('contact.html')
    
        return app
