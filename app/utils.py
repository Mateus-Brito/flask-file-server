from .models import User
from .database import db

def userAlreadyExist( email ):
    return User.query.filter_by(email=email).count() > 0

def passwordsAreIdentical( password1, password2):
    return password1 == password2

def registerUser( form ):

    if userAlreadyExist( form.email.data ):
        message = {'message': "Este email já está cadastrado"}
        result_code = 400

    elif passwordsAreIdentical(form.password.data, form.rpassword.data):
        message = {'message': "As senhas digitadas são diferentes"}
        result_code = 400

    else:
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, \
                    email=form.email.data, password=form.password.data)

        db.session.add(user)
        db.commit()

        message = {'message': "Cadastro realizado"}
        result_code = 200

    return (message, result_code)