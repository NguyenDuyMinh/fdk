# -*- coding: utf-8 -*-
from flask import Flask
from wtforms import SelectMultipleField, StringField, BooleanField, widgets, HiddenField
from wtforms.validators import required, email, regexp, optional
from wtforms.widgets import TextArea
from flask_wtf import Form
from server.models import database
from bson import ObjectId

class ProductForm(Form):
	"""docstring for ClassName"""
	proId = HiddenField(u'')
	name = StringField(u'物件名')
	price = StringField(u'価格')
	type = StringField(u'タイプ')
	description = StringField(u'説明', widget=TextArea())
	image = StringField(u'ホームページ')

	def __init__(self, arg):
		super(ProductForm, self).__init__()
		self.arg = arg
		if self.arg:
		 	self.mapping_form()

	def mapping_form(self):
		pro = self.get_product()
		self.proId.data = pro['_id']
		self.name.data = pro['name']
		self.price.data = pro['price']
		self.type.data = pro['type']
		self.description.data = pro['description']
		self.image.data = pro['image']
		return True

	def get_product(self):
		pro_id = self.arg['pro_id']
		mongodb = database.get_config_mongo()
		proIds = set(ObjectId(x.strip()) for x in pro_id.split(',') if x.strip())
		for proId in proIds:
			pro = mongodb.products.find_one({'_id': proId });
		return pro