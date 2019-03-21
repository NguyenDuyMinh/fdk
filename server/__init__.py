# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for, redirect, session
from server.forms.admin_form import AdminForm
from server.models.users import Admin
from server.models import database
import os

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    Admin.init_db()
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

    @app.route('/dashboard')
    def dashboard():
        form = AdminForm(request.form)
        if 'username' in session:
            username = session['username']
            return render_template('dashboard.html', username=username)
        return redirect(url_for('.login'))
    return app

