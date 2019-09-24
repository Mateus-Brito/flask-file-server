from flask import Blueprint, render_template, current_app, session
from app.socketio import socketio

from flask_socketio import send, emit
from flask_socketio import join_room, leave_room
from werkzeug.utils import secure_filename

from flask_login import current_user, login_required

from app.views import authenticated_only
from app.utils import createRootUser
from app.mod_drive.rc4 import rc4
from urllib.parse import unquote 

import sys
import shutil
import os
import re
import base64
import json
from PIL import Image
from io import BytesIO
import uuid
import hashlib
import secrets

getHash256 = lambda text : hashlib.sha256( str(text).encode("UTF-8")).hexdigest()
secretsGenerator = secrets.SystemRandom()

mod_drive = Blueprint('drive', __name__,template_folder='templates')

def preventBackDir( path ):
    path_modified = str(path).replace("/../", "")
    path_modified  = re.sub(r'^../', "",path_modified)
    path_modified  = re.sub(r'/..$', "",path_modified)
    path_modified  = re.sub(r'^..$', "",path_modified)

    return path_modified

@mod_drive.route('/')
@login_required
def index():
    session['uid'] = uuid.uuid4()
    session['secret'] = secretsGenerator.randint(2,50)
    session['public'] = (12 ** int(session['secret']) ) % 13
    return render_template('portal/index.html', session_uid=session['uid'])

@socketio.on('join')
def on_join(data):
    room = current_user.uuid
    join_room(room)

    public_key = int( data['shared'] )
    my_private_key = int( session['secret'] )

    session['shared'] = ( public_key ** my_private_key ) % 13

    emit('shared', {
        'shared': session['public']
    })

    emit('load_content', {
        'folders': getFolderList(''),
        'files': getFileList(''),
    })

@socketio.on('change_page')
def changePage( json_obj ):
    path = preventBackDir( json_obj['data']['path'] )
    
    emit('load_content', {
        'folders': getFolderList(path),
        'files': getFileList(path),
    })

@socketio.on('new_folder')
@authenticated_only
def makeFolder( json_obj ):

    hash = getHash256( json_obj['data']['filename'] + str(session['uid']) )

    if hash != json_obj['data']['hash']:
        #cancel
        print("hahahahahhaha", file=sys.stderr)
        return

    createFolder( json_obj['data']['filename'], json_obj['data']['path'])

@socketio.on('delete_items')
@authenticated_only
def deleteItems( json_obj ):

    hash = getHash256( str(json_obj['data']['files']) + str(json_obj['data']['folders']) + str(session['uid']) )

    if hash != json_obj['data']['hash']:
        #cancel
        return

    files = json.loads( json_obj['data']['files'] )
    folders = json.loads( json_obj['data']['folders'] )
    
    removeFiles( files, json_obj['data']['path'])
    removeFolders( folders, json_obj['data']['path'])

@socketio.on('new_file')
@authenticated_only
def handle_my_custom_event(json_obj):

    decrypted_file = unquote(unquote( rc4( unquote(unquote(json_obj['data']['base64File'] ))) )).encode('utf-8').decode("utf-8")
    decrypted_hash = rc4( unquote(unquote(json_obj['data']['hash'] ))).encode('utf-8').decode("utf-8")

    hash = getHash256( decrypted_file  + str(session['uid']) )
   
    if hash != decrypted_hash:
        #cancel
        print("oxeeeeeeeeeee!!!!!!!!!", file=sys.stderr)
        return

    if 'fileName' in json_obj['data']:
        save_file( json_obj['data']['fileName'], decrypted_file, json_obj['data']['path'] )

def save_file(filename, b64_string, path):
    createRootUser()
    path = preventBackDir( path )
    path_file = current_app.config['DRIVE_FOLDER'] + f"{str(current_user.uuid)}/{path}/" + secure_filename( filename )

    filename, file_extension = os.path.splitext( path_file )
    file_extension = str(file_extension).lower()
    
    b64_string = b64_string[ b64_string.find(",")+1 :]

    byte_data = base64.b64decode( b64_string )

    with open(path_file, "wb") as f:
        f.write( byte_data )

    #emit event    
    createFile( filename )
    
def createFile( name ):
    name = os.path.basename( name )
    emit('file_added', {
        'data': {
            'name': name,
        }
    }, room=current_user.uuid)

def createFolder( name, path ):
    createRootUser()
    
    name = secure_filename(name)
    path = preventBackDir( path )
    directory = current_app.config['DRIVE_FOLDER'] + f"{current_user.uuid}/{path}/{name}" 

    if not os.path.exists( directory ):
        os.makedirs(directory)

    emit('folder_added', {
        'data': {
            'name': name,
        }
    }, room=current_user.uuid)

def getFolderList( path ):
    path = current_app.config['DRIVE_FOLDER'] + f"/{str(current_user.uuid)}/" + preventBackDir( path )

    return [o for o in os.listdir(path) if os.path.isdir(os.path.join(path,o))]

def getFileList( path ):
    path = current_app.config['DRIVE_FOLDER'] + f"/{str(current_user.uuid)}/" + preventBackDir( path )

    return [o for o in os.listdir(path) if not os.path.isdir(os.path.join(path,o))]

def removeFiles( items, path):
    path = current_app.config['DRIVE_FOLDER'] + f"/{str(current_user.uuid)}/" + preventBackDir( path )

    for item in items:
        file_path = f"{path}/{item}"
        if os.path.isfile( file_path ):
            os.remove( file_path )
    
    emit('file_removed', {
        'data': {
            'files': json.dumps( items ),
        }
    }, room=current_user.uuid)
    
def removeFolders( items, path):
    path = current_app.config['DRIVE_FOLDER'] + f"/{str(current_user.uuid)}/" + preventBackDir( path )

    for item in items:
        file_path = f"{path}/{item}"
        
        if os.path.isdir( file_path ):
            shutil.rmtree(file_path, ignore_errors=True)

    emit('folder_removed', {
        'data': {
            'folders': json.dumps( items ),
        }
    }, room=current_user.uuid)