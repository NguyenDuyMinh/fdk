# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymongo


def get_config_sql():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/test'
    db = SQLAlchemy(app)
    return db

def get_config_mongo():
    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    mydb = myclient["fdk-dev"]
    mycol = mydb["estates_baibai"]
    return mycol
    # xs = mycol.find(myquery, myresult).limit(3)
    # return CursorWrapper(SaleEstateWidget, xs)
