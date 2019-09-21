from flask import Blueprint, render_template, current_app
from app.socketio import socketio
from werkzeug.utils import secure_filename

from flask_login import current_user, login_required

from app.views import authenticated_only
from app.utils import createRootUser

import sys
import os
import re
import base64
from PIL import Image
from io import BytesIO

mod_drive = Blueprint('drive', __name__,template_folder='templates')

@mod_drive.route('/')
@login_required
def index():
    return render_template('portal/index.html')

@socketio.on('my event')
@authenticated_only
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    if 'fileName' in json['data']:
        save_file( json['data']['fileName'], json['data']['base64File']  )

def save_file(filename, b64_string):
    createRootUser()
    path_file = current_app.config['DRIVE_FOLDER'] + f"/{str(current_user.uuid)}/" + secure_filename( filename )

    filename, file_extension = os.path.splitext( path_file )
    file_extension = str(file_extension).lower()

    if b64_string[-1:] != "=":
        b64_string += "=="

    if file_extension == ".txt":
        b64_string = b64_string.replace("data:text/plain;base64,", "")

    elif file_extension == ".png":
        b64_string = re.sub('^data:image/.+;base64,', '', b64_string)
        byte_data = base64.b64decode( b64_string )

        image_data = BytesIO( byte_data )
        img = Image.open(image_data)
        img.save(path_file , "PNG")
        return

    byte_data = base64.b64decode( b64_string )

    with open(path_file, "wb") as f:
        f.write( byte_data )
    