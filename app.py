from flask import Flask
from config import config
from mongoengine import connect
from api.v1.controller import controller as api_v1


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # mongo.init_app(app)
    connect(host=app.config['MONGO_URI'])
    
    # if app.config['DEBUG']:
        # from test.controllers import test_blueprint 
        # app.register_blueprint(test_blueprint, url_prefix='/test')
    app.register_blueprint(api_v1, url_prefix='/api/v1')

    return app
