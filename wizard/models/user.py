# The User Model

from wizard import db


class User(db.Model):
    __tablename__ = 'users'
    usr_id = db.Column(db.Integer(), primary_key=True)
    usr_email = db.Column(db.String(150), unique=True)
    usr_name = db.Column(db.String(150), unique=True)
    usr_password = db.Column(db.String(250))
    usr_active_status = db.Column(db.String(1))
