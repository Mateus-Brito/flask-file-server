from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import current_user
from flask_socketio import disconnect

import functools
import sys
from app.socketio import socketio

from .forms import Register
from .models import User
from .database import db

from .utils import registerUser

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


@file_server.route('/login')
def login():
    return render_template("login.html")

@file_server.route('/register', methods=['GET', 'POST'])
def register():
    form = Register(request.form)

    if request.method == 'POST' and form.validate():
        
        result = registerUser( form )
        print( result, file=sys.stderr)

        return jsonify( result )

    if form.errors :
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                return jsonify({'message': str(err), 'id': fieldName}), 400

    return render_template("register.html", form=form)