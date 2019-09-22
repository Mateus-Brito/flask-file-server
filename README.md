## Basic file server written in flask

![default_drive](https://user-images.githubusercontent.com/13570164/65382180-8a6c2a00-dcd5-11e9-8acc-d8e843c64343.png)


## Commands:

create a .env file in the project root folder with the following content:
```
FLASK_APP = 'run.py'
FLASK_ENV=development

FLASK_SECRET_KEY=<anything>

FLASK_SQLALCHEMY_DATABASE_URI=sqlite:////tmp/test.db

```

if you don't have it, install pipenv
```
pip install pipenv
```

and after that:

```
pipenv install
pipenv run python run.py
```

to initialize the database:
```
pipenv run flask db init
pipenv run flask db migrate
pipenv run flask db upgrade
```

for tests:
```
pipenv run pytest tests/
```