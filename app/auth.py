import sys
import uuid

from .models import User
from .database import db

from flask_login import login_user

def userAlreadyExist( email ):
    return db.session.query(User.id).filter_by(email=email).count() > 0

def passwordsAreIdentical( password1, password2):
    return password1 == password2

def registerUser( form ):

    if not passwordsAreIdentical(form.password.data, form.rpassword.data):
        message = "As senhas digitadas são diferentes"
        result_code = 400

    elif userAlreadyExist( form.email.data ):
        message = "Este email já está cadastrado"
        result_code = 400

    else:
        own_uuid = str(uuid.uuid4())
        user = User(uuid=own_uuid,first_name=form.first_name.data, last_name=form.last_name.data, \
                    email=form.email.data, password=form.password.data)

        db.session.add(user)
        db.session.commit()

        message = "Cadastro realizado"
        result_code = 200

    return {'message': message}, result_code

def loginUser( email, password ):

    message = ""
    code = 200

    user = User.query.filter_by(email=email, password=password).first()

    if user:
        login_user( user )
        message = "Autenticação realizada."
        code = 200
    else:
        message = "Email ou senha invalido."
        code = 400

    return {'message': message}, code