from flask import Blueprint, render_template, redirect, url_for, request, jsonify, current_app, session

from flask_login import current_user
from flask_socketio import disconnect

import functools

import sys
import os
from app.socketio import socketio
from flask_login import logout_user

from .forms import Register, Login
from .models import User
from .database import db
from .utils import createRootUser

file_server = Blueprint('file_server', __name__,template_folder='templates')

def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped

@file_server.route('/')
def index():
    return redirect( url_for('file_server.login') )

@file_server.route('/logout')
def logout():
    logout_user()
    return redirect( url_for('file_server.login'))

@file_server.route('/login', methods=['GET'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for("drive.index"))

    form = Login(request.form)

    return render_template("login.html", form=form)

@file_server.route('/register', methods=['GET'])
def register():
    form = Register(request.form)

    return render_template("register.html", form=form)