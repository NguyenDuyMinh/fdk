# -*- coding:utf-8 -*-
from wtforms import StringField, PasswordField, SubmitField, HiddenField, SelectField, Form
from wtforms.validators import required, EqualTo
from wtforms.fields import BooleanField

class AdminForm(Form):
	username = StringField(u'ユーザー名')
	email = StringField(u'メールアドレス', [required()])
	password = PasswordField(u"パスワード", [required(), EqualTo('password_confirm', message=u'パスワードが一致しません。')])
	password_confirm = PasswordField(u"パスワード再入力", [required()])
	role = SelectField(u'役割', choices=[('', '選択肢'), ('1', 'admin'), ('2', 'subadmin') ])
	submit = SubmitField('新規会員登録')
	hidden_tag = HiddenField()