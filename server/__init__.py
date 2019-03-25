# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for, redirect, session
from server.forms.admin_form import AdminForm
from server.forms.product_form import ProductForm
from server.models.users import Admin
from server.models import database
import os
from bson import ObjectId

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    Admin.init_db()
    mongodb = database.get_config_mongo()
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return redirect(url_for('.dashboard'))

    # login
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = AdminForm(request.form)
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            admin = Admin.query.filter_by(email=email, password=password).first()
            if admin:
                username = admin.username
                session['username'] = username
                return redirect(url_for('.dashboard'))
            raise(u'hure')
        return render_template('admin/login.html', form=form)
        
    # register
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = AdminForm(request.form)
        db = database.get_config_sql()
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            admin = Admin(username, email, password)
            if admin:
                db.session.add(admin)
                db.session.commit()
                session['username'] = username
                return render_template('dashboard.html')
        return render_template('admin/register.html', form=form)

    # register
    @app.route('/logout', methods=['GET', 'POST'])
    def logout():
        session.pop('username', None)
        return redirect(url_for('login'))

    @app.route('/dashboard', methods=['GET', 'POST '])
    def dashboard():
        context = []
        pros = mongodb.products.find({})    
        if pros:
            context.append(pros)

        if 'username' in session:
            username = session['username']
            return render_template('dashboard.html', context=context)   
        return redirect(url_for('.login'))

    # create product
    @app.route('/create', methods=['GET', 'POST'])
    def create():
        type_form = '/create'
        if request.method == 'POST':
            fields = {
                'name': request.form['name'], 
                'price': request.form['price'], 
                'type': request.form['type'],
                'description': request.form['description'],
                'image': request.form['img']
            }
            try:
               mongodb.products.insert_one(fields);
               return redirect(url_for('.dashboard'))
            except:
               print("Can not create")
        form = ProductForm(request.values)
        return render_template('products/index.html', form=form, type_form=type_form)

    # edit product
    @app.route('/edit', methods=['GET', 'POST'])
    def edit():
        type_form = '/edit'
        if request.method == 'POST':
            pro_id = request.form['proId']
            proId = set(ObjectId(x.strip()) for x in pro_id.split(',') if x.strip())
            fields = {
                'name': request.form['name'], 
                'price': request.form['price'], 
                'type': request.form['type'],
                'description': request.form['description'],
                'image': request.form['img']
            }
            try: 
                mongodb.products.update_one({'_id': {'$in': list(proId)}}, { '$set': fields })
                return redirect(url_for('.dashboard'))
            except:
                print("Can not create")
        if not request.values:
            return redirect(url_for('.dashboard'))
        form = ProductForm(request.values)
        return render_template('products/index.html', form=form, type_form=type_form)

    # remove product
    @app.route('/remove', methods=['GET'])
    def remove():
        pro_id = request.values['pro_id']
        proId = set(ObjectId(x.strip()) for x in pro_id.split(',') if x.strip())
        try: 
            mongodb.products.delete_one({'_id': {'$in': list(proId)}})
            return redirect(url_for('.dashboard'))
        except:
            print("Can not remove")

    # detail product
    @app.route('/info', methods=['GET'])
    def info():
        form = ProductForm(request.values)
        return render_template('products/info.html', form=form) 
        
    return app

