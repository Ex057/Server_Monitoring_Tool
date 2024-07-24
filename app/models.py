from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db
#db = SQLAlchemy()

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    servers = db.relationship('Server', backref='owner', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):  # Implement get_id
        return str(self.id)

    def __repr__(self):
        return f'<User {self.username}>'

class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    ip_address = db.Column(db.String(64))
    user_name = db.Column(db.String(64))
    password = db.Column(db.String(64))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    last_checked = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f'<Server {self.name}>'
    

class test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(64), db.ForeignKey('server.ip_address'))
    user_name = db.Column(db.String(64), db.ForeignKey('server.user_name'))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'),default=None)
    available = db.Column(db.String(64))
    analytics = db.Column(db.String(64))
    dashboards = db.Column(db.String(64))
    testTime = db.Column(db.DateTime, default=datetime.now())
    last_checked = db.Column(db.DateTime, default=None)

    def __repr__(self):
        return f'<test {self.id}>'