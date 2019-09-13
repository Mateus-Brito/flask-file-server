from flask import Blueprint, render_template
from flask_login import current_user
from flask_socketio import disconnect

import functools
from app.socketio import socketio

file_server = Blueprint('file_server', __name__,template_folder='templates')

def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped

