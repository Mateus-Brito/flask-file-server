from wtforms import Form, StringField, PasswordField, validators

class Register(Form):
    first_name = StringField('Nome', [validators.Length(min=4, max=25,message="O nome deve conter entre 4 e 25 caracteres.")])
    last_name = StringField('Sobrenome', [validators.Length(min=4, max=25,message="O sobrenome deve conter entre 4 e 25 caracteres.")])
    email = StringField('Email', [validators.Length(min=4, max=120, message="Email é obrigatório.")])
    password = PasswordField('Senha', [validators.Length(min=4, max=25,message="A senha deve conter entre 4 e 25 caracteres.")])
    rpassword = PasswordField('Confirmar senha', [validators.Length(min=4, max=25, message="As senhas devem ser idênticas.")])

class Login(Form):
    email = StringField('Email', [validators.Length(min=4, max=120, message="Email é obrigatório.")])
    password = PasswordField('Senha', [validators.Length(min=4, max=25,message="A senha deve conter entre 4 e 25 caracteres.")])