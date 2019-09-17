from flask import Blueprint, render_template
from app.socketio import socketio
from app.views import authenticated_only

import sys

mod_drive = Blueprint('drive', __name__,template_folder='templates')

@mod_drive.route('/')
def login():
    return render_template('portal/index.html')

@socketio.on('my event')
@authenticated_only
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    print('----------------- ', file=sys.stderr)