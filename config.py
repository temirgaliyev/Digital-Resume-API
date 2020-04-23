# import os

# basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = ''

    @staticmethod
    def init_app(app):
        pass


class MainConfig(BaseConfig):
    DEBUG = False
    MONGO_URI = "mongodb+srv://default_user:somerandompassword@cluster0-o3l0x.mongodb.net/test?retryWrites=true&w=majority"


class DebugConfig(BaseConfig):
    DEBUG = True
    
    MONGO_URI = "mongodb+srv://default_user:somerandompassword@cluster0-o3l0x.mongodb.net/test?retryWrites=true&w=majority"


config = {
    'main': MainConfig,
    'debug': DebugConfig
}