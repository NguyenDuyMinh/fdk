# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from server.models import database
db = database.get_config_sql()

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), unique=True)
    role = db.Column(db.Integer)

    def __init__(self, username, email, password, role):
        self.username = username
        self.email = email
        self.password = password
        self.role = role

    def __repr__(self):
        return '<User %r>' % self.username

    def check_duplicate():
        admin = query.filter_by(email=self.email, password=self.password).first()
        if admin:
            return False
        return True

    def init_db():
        return db.create_all()