# flask-file-server

## Commands:

create a .env file in the project root folder with the following content:
```
FLASK_APP = 'run.py'
FLASK_ENV=development

FLASK_SECRET_KEY=<any thing>
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


```
pipenv run flask db init
pipenv run flask db migrate
pipenv run flask db upgrade
```