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
        from test.controllers import test  
        app.register_blueprint(test, url_prefix='/test')

    return app
