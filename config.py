# import os
# basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = ''

    @staticmethod
    def init_app(app):
        pass


class MainConfig(BaseConfig):
    DEBUG = False
    MONGO_URI = ""


class DebugConfig(BaseConfig):
    DEBUG = True
    MONGO_URI = ""


config = {
    'main': MainConfig,
    'debug': DebugConfig
}