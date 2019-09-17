from flask import Flask
from flask_login import LoginManager
from dynaconf import FlaskDynaconf
from app.socketio import socketio

from flask_migrate import Migrate

from app.views import file_server
from .mod_drive import mod_drive

from .database import db

from itsdangerous import URLSafeTimedSerializer

def create_app():

    app = Flask(__name__, static_folder='static')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.url_map.strict_slashes = False

    FlaskDynaconf(app)

    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.session_protection = "strong"

    login_manager.login_view = "user"
    login_manager.refresh_view = "user"
    login_manager.needs_refresh_message = (
        u"Para proteger sua conta, por favor autentique novamente para acessar esta página."
    )
    login_manager.needs_refresh_message_category = "info"

    app.register_blueprint(file_server, url_prefix='/')
    app.register_blueprint(mod_drive, url_prefix='/drive')

    socketio.init_app(app)

    return app