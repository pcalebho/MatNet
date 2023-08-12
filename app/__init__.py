''''
factory function to create the app
'''

import os

from flask import Flask

def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'development'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from models import db
    db.init_app(app)

    with 

    from routes.api import api_bp
    from routes.docs import docs_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(docs_bp)
    
    # from routes.main import main_bp

    @app.route('/')
    def hello():
        return 'Hello World'


    return app
