from flask import current_app
from flask_login import current_user
import os

def createRootUser():
    directory = current_app.config['DRIVE_FOLDER'] + str(current_user.uuid)
    if not os.path.exists( directory ):
        os.makedirs(directory)