from flask import Flask
from flask_pymongo import PyMongo
from config import config

mongo = PyMongo(app)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mongo.init_app(app)
    
    return app


if __name__ == '__main__':
    application = create_app('debug')
    application.run()