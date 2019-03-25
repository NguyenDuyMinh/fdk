# -*- coding:utf-8 -*-
from wtforms import StringField, PasswordField, SubmitField, HiddenField, Form
from wtforms.validators import required, EqualTo

class AdminForm(Form):
	username = StringField(u'ユーザー名')
	email = StringField(u'メールアドレス', [required()])
	password = PasswordField(u"パスワード", [required(), EqualTo('password_confirm', message=u'パスワードが一致しません。')])
	password_confirm = PasswordField(u"パスワード再入力", [required()])
	submit = SubmitField('新規会員登録')
	hidden_tag = HiddenField()