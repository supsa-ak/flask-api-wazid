# from werkzeug.wrappers import request
from sqlalchemy.sql.operators import exists
from app import *

class Add_customer(Resource):    
    def post(self):
        c = Customer(name=request.json['name'], username=request.json['username'], password=request.json['password'], level=request.json['level'])
        db.session.add(c)
        db.session.commit()
        print(session)
        return {"message": 'customer created with name '+request.json['name']}, 201

class Login(Resource):    
    def post(self):
        if session['username']:
            return {"message": 'Already Logged in as '+ session['username']}, 200
        else:
            try:
                uname = request.json['username']
                pword = request.json['password']
                if Customer.query.filter_by(username=uname).first():
                    custom = Customer.query.filter_by(username=uname).first()
                    if Customer.query.get(custom.cust_id).password == pword:
                        # print(session)
                        session['username'] = uname
                        # print(session)
                        return {"message": 'Successfully Logged in as '+ uname}, 201
            except:
                    return  {"message": 'Incorrect Username or Password'}, 200

class Logout(Resource):    
    def get(self):      
        session['username'] = None
        print('thisis ', session)
        return {"message":"User Logged Out"}
    def post(self):      
        session['username'] = None
        # session.pop('username',None)
        return {"message":"User Logged Out"}

class Add_vendor(Resource):
    def post(self):
        # print(session)
        # print(session['username'])
        if session['username']:
            return {"message": 'Login Required'}
        else:
            pass 
        data = Vendor(cust_id=request.json['cust_id'], restaurant_name=request.json['restaurant_name'])
        db.session.add(data)
        db.session.commit()
        return {"message": 'Vendor created with restaurant name '+request.json['restaurant_name']}, 201

class Get_all_vendors(Resource):
    def get(self):
        if session['username']:
            pass
        else:
            return {"message": 'Login Required'}

        vendors = Vendor.query.all()
        params = []
        # params2 = []
        m = 0
        for i in vendors:
            print(m)
            id = i.vendor_id
            vendor_info = {"vendor_id":i.vendor_id, "cust_id":i.cust_id, "restaurant_name":i.restaurant_name, "data":[]}
            params.append(vendor_info)

            res = db.session.query(Food).filter_by(vendor_id=id).all()
            for j in res:
                dict = {"food_id":j.food_id, "vendor_id":j.vendor_id, "dish_name":j.dish_name, "calories_per_gm":j.calories_per_gm, "available_quantity":j.available_quantity, "unit_price":j.unit_price}
                print(dict)
                params[m]['data'].append(dict)
            # params["data"] = params2
            m = m+1
            
        return params, 200

class Add_item(Resource):
    def post(self):
        if session['username']:
            return {"message": 'Login Required'}
        else:
            pass 
        username = session['username'] 
        cust_info = session.query.filter_by(username).first()
        if Vendor.query.filter_by(cust_id=cust_info.cust_id).first():
            food = Food(food_id=request.json['food_id'], vendor_id=request.json['vendor_id'], 
                        dish_name=request.json['dish_name'], calories_per_gm=request.json['calories_per_gm'],
                        available_quantity=request.json['available_quantity'],unit_price=request.json['unit_price'])
            db.session.add(food)
            db.session.commit()
            return {"message": 'Item added Successfully'}, 200
        else:
            return {"message": 'Don\'t have required privileges'}, 404

class Place_order(Resource):
    def post(self):
        if session['username']:
            return {"message": 'Login Required'}
        else:
            pass 
        order = Orders(cust_id=request.json['cust_id'], item_id=request.json['item_id'], quantity=request.json['quantity'])


class Get_all_orders_by_customer(Resource):
    def get(self):
        if session['username']:
            return {"message": 'Login Required'}
        else:
            pass 
        id = request.json['id']
        all_orders = db.session.query(Orders).filter_by(cust_id=id).all()
        params = {}
        for i in all_orders:
            params2 = {"order_id":i.order_id, "cust_id":i.cust_id, "total_amount":i.total_amount, "date":i.date}
            params.update(params2)
        return params, 200

class Get_all_orders(Resource):
    def get(self):
        if session['username']:
            return {"message": 'Login Required'}
        else:
            pass 
        uname = session['username']
        cust_info = Customer.query.filter_by(username=uname).first()
        if cust_info.level == 2:
            all_orders = Orders.query.all()
            return 'ok', 200
        else: 
            return {"message": 'Don\'t have required privileges'}, 404

api.add_resource(Add_customer, '/addcustomer')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Add_vendor, '/addvendor')
api.add_resource(Get_all_vendors, '/getallvendors')
api.add_resource(Add_item, '/additem')
api.add_resource(Place_order, '/placeorder')
api.add_resource(Get_all_orders_by_customer, '/getallordersbycustomer')
api.add_resource(Get_all_orders, '/getallorders')

# {   
#     "name": "sarthak",
#     "username": "sak",
#     "password": "123",
#     "level":1
# }

# {
#     "username": "sak",
#     "password": "123"
# }

# {
#     "cust_id": 2
#     "restaurant_name": 'dominos'
# }