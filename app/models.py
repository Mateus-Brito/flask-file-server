from .database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    @property
    def is_admin(self):
        return False

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User>'