from flask import current_app
from flask_login import current_user
import os

def createRootUser( uuid_user ):
    directory = current_app.config['DRIVE_FOLDER'] + str(uuid_user)
    if not os.path.exists( directory ):
        os.makedirs(directory)