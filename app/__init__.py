from flask import Flask, jsonify, redirect, url_for, _request_ctx_stack, request, session
import os

from flask_login import LoginManager
from dynaconf import FlaskDynaconf
from app.socketio import socketio

from flask_migrate import Migrate
from flask_wtf.csrf import CSRFError
from .JWTManager import jwt

from app.views import file_server
from .mod_drive import mod_drive

from .database import db
from .csrf_protection import csrf
from .models import User

from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv

load_dotenv()

def create_app():

    app = Flask(__name__, static_folder='static')
    app.config['JWT_SECRET_KEY'] = 'super-secret'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.url_map.strict_slashes = False

    FlaskDynaconf(app)
    createDefaultConfig( app )
    
    db.init_app(app)
    csrf.init_app(app)
    jwt.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.session_protection = "strong"
    login_serializer = URLSafeTimedSerializer(app.secret_key)

    login_manager.login_view = "user"
    login_manager.refresh_view = "user"
    login_manager.needs_refresh_message = (
        u"Para proteger sua conta, por favor autentique novamente para acessar esta página."
    )
    login_manager.needs_refresh_message_category = "info"

    app.register_blueprint(file_server, url_prefix='/')
    app.register_blueprint(mod_drive, url_prefix='/drive')

    socketio.init_app(app)
    
    @app.before_request
    def set_domain_session():
        session['domain'] = request.headers['Host']

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return jsonify({'message': "Token expirado, por favor atualize a página!"}), 400

    @login_manager.unauthorized_handler
    def unauthorized_handler():
        return redirect(url_for("file_server.login"))

    return app

def createDefaultConfig( current_app ):
    directory = current_app.config['DRIVE_FOLDER']
    if not os.path.exists( directory ):
        os.makedirs(directory)