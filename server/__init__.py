# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for, redirect, session
from server.forms.admin_form import AdminForm
from server.forms.product_form import ProductForm
from server.models.users import Admin
from server.models import database
import os
from bson import ObjectId
import datetime
import dateutil.parser as dp

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
                session['username'] = admin.username
                session['role'] = admin.role
                return redirect(url_for('.dashboard'))
            message = u'ログインできません。'
            return render_template('admin/auth/login.html', form=form, message=message)
        return render_template('admin/auth/login.html', form=form)
        
    # register
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = AdminForm(request.form)
        db = database.get_config_sql()
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            role = request.form['role']
            admin = Admin(username, email, password, role)
            if admin:
                try:
                    db.session.add(admin)
                    db.session.commit()
                    session['username'] = username
                    session['role'] = role
                    return redirect(url_for('.dashboard'))
                except:
                    message = u'登録できません。'
                    return render_template('admin/auth/register.html', form=form, message=message)
        return render_template('admin/auth/register.html', form=form)

    # register
    @app.route('/logout', methods=['GET', 'POST'])
    def logout():
        session.pop('username', None)
        session.pop('role', None)
        return redirect(url_for('login'))

    @app.route('/dashboard', methods=['GET', 'POST '])
    def dashboard():
        context = []
        pros = mongodb.products.find({})   
        if pros:
            context.append(pros)

        if 'username' in session:
            username = session['username']
            return render_template('admin/dashboard.html', context=context)   
        return redirect(url_for('.login'))

    # create product
    @app.route('/create', methods=['GET', 'POST'])
    def create():
        type_form = '/create'
        if request.method == 'POST':
            current_date = datetime.datetime.now()
            fields = {
                'name': request.form['name'], 
                'price': request.form['price'], 
                'type': request.form['type'],
                'description': request.form['description'],
                'image': request.form['img'],
                'date_created': current_date
            }
            try:
               mongodb.products.insert_one(fields);
               return redirect(url_for('.dashboard'))
            except:
               print("Can not create")
        form = ProductForm(request.values)
        return render_template('admin/products/index.html', form=form, type_form=type_form)

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
        return render_template('admin/products/index.html', form=form, type_form=type_form)

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

    # home
    @app.route('/home', methods=['GET'])
    def home():
        context = {}
        today = datetime.datetime.now()
        parsed_t = dp.parse(str(today))
        current_date = parsed_t.isoformat()
        seven_date_before = today - datetime.timedelta(days=7)
        parsed_t = dp.parse(str(seven_date_before))
        week_ago = parsed_t.isoformat()
        # {'date_created': {"$lte": arg}}
        # {'date_created': {"$lte": arg}}
        # {'date_created': 2 {"$lte": arg}}
        # {'date_created': 3 {"$lte": arg}}
        # {'date_created': 4 {"$lte": arg}}
        # {'date_created': 5 {"$lte": arg}}
        pros_new = mongodb.products.find()
        if pros_new:
            context['pros_new'] = pros_new

        return render_template('site/index.html', context=context) 

    # introducation
    @app.route('/introducation', methods=['GET'])
    def introducation():
        return render_template('site/introducation.html')

    # product
    @app.route('/product', methods=['GET'])
    def product():
        return render_template('site/product.html')
        
    # product
    @app.route('/contact', methods=['GET'])
    def contact():
        return render_template('site/contact.html')

    # product
    @app.route('/notice', methods=['GET'])
    def notice():
        return render_template('site/notice.html')
    return app