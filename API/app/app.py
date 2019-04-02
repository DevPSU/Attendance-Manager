from flask import Flask, Blueprint, jsonify
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_cors import CORS

from shutil import copyfile
import os
import configparser
import importlib

from sqlalchemy.engine import Engine
from sqlalchemy import event

def error_json(error, error_code):
    return jsonify({'error': error}), error_code

application = Flask(__name__)
CORS(application, supports_credentials=True)
bcrypt = Bcrypt(application)

basedir = os.path.abspath(os.path.dirname(__file__))

appenv = os.environ.get('APP_ENV')
config = configparser.ConfigParser()
config.read('app/config.ini')

if appenv != 'development' and appenv is not None:
    if appenv not in config:
        print("ERROR: You must add details for this environment to config.ini.")
    else:
        host = config[appenv]['host']
        db = config[appenv]['db']
        username = config[appenv]['username']
        password = config[appenv]['password']

        application.secret_key = config[appenv]['secret']
        application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+ username +':'+ password +'@'+ host + '/' + db + "?charset=utf8mb4"
else:
    sqlite_path = os.path.join(basedir, 'development-db.sqlite')
    # Moves the sqlite db to a folder that we can read/write in Lambda
    if os.environ.get('USING_ZAPPA') is not None:
        src = os.path.join(basedir, 'development-db.sqlite')
        sqlite_path = "/tmp/development-db.sqlite"
        copyfile(src, sqlite_path)

    application.secret_key = config['development']['secret']
    application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + sqlite_path


    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

# Custom configurations
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['OUR_EPOCH'] = 1531953129


from .Models import db
db.init_app(application)
migrate = Migrate(application, db)

# Automatically import endpoints from Endpoints folder
for file in os.listdir(os.path.dirname(__file__)+'/Endpoints/'):
    # Import the module
    module_name = file[:-3]   # strip .py at the end
    if not module_name[0].isalpha():
        continue
    try:
        module = importlib.import_module('.'+module_name, package='app.Endpoints')
    except ModuleNotFoundError as e:
        # Not a real module
        continue
    globals()[module_name] = module

    # Register the module's Blueprint
    unregistered = True
    for attr in dir(module):
        potential_blueprint = getattr(module, attr)
        if isinstance(potential_blueprint, Blueprint):
            application.register_blueprint(potential_blueprint)
            unregistered = False
            break

    if unregistered is True:
        print("ERROR: Unable to register blueprint for module '" + module_name + "'.")
        print("\tThe file must start with (update file_name): file_name = Blueprint('file_name', __name__)")

if __name__ == '__main__':
    application.run(debug=True)
