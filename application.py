from flask import Flask
from flask_pymongo import PyMongo
from config import config

mongo = PyMongo()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mongo.init_app(app)
    
    if app.config['DEBUG']:
        from test.controllers import test_blueprint 
        from api.controllers import api_blueprint 
        app.register_blueprint(test_blueprint, url_prefix='/test')
        app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
