import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.environ["FLASK_basedir"] = basedir

os.environ["FLASK_DRIVE_FOLDER"] = basedir+'/drive_database/'

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')