from app import application
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///..\FlaskRestaurant.sqlite3'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(application)

class Customer(db.Model):
    __tablename__ = 'customer'
    cust_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    username = db.Column(db.String)
    password = db.Column(db.String)
    level = db.Column(db.Integer)

    def __init__(self, name, username, password, level):
    	self.name = name
    	self.username = username
    	self.password = password
    	self.level = level

class Vendor(db.Model):
    __tablename__ = 'vendor'
    vendor_id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer, db.ForeignKey("customer.cust_id"))
    restaurant_name = db.Column(db.String)

    def __init__(self, vendor_id, cust_id, restaurant_name):
    	self.cust_id = cust_id
    	self.restaurant_name = restaurant_name

class Food(db.Model):
    __tablename__ = 'food'
    food_id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey("vendor.vendor_id"))
    dish_name = db.Column(db.String)
    calories_per_gm = db.Column(db.Integer)
    available_quantity = db.Column(db.Integer)
    unit_price = db.Column(db.Integer)

    def __init__(self, food_id, vendor_id, dish_name, calories_per_gm, available_quantity, unit_price):
    	self.food_id = food_id
    	self.vendor_id = vendor_id
    	self.dish_name = dish_name
    	self.calories_per_gm = calories_per_gm
    	self.available_quantity = available_quantity
    	self.unit_price = unit_price

class Orders(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer, db.ForeignKey("customer.cust_id"))
    total_amount = db.Column(db.Integer)
    date = db.Column(db.Date)

    def __init__(self, order_id, cust_id, total_amount, date):
    	self.order_id = order_id
    	self.cust_id = cust_id
    	self.total_amount = total_amount
    	self.date = date

class OrderItems(db.Model):
    __tablename__ = 'orderItems'
    item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.order_id"))
    food_id = db.Column(db.Integer, db.ForeignKey("food.food_id"))
    quantity = db.Column(db.Integer)
    amount = db.Column(db.Integer)

    def __init__(self, item_id, order_id, food_id, quantity, amount):
    	self.item_id = item_id
    	self.order_id = order_id
    	self.food_id = food_id
    	self.quantity = quantity
    	self.amount = amount

db.create_all()
db.session.commit()