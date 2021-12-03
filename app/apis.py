from app import *

class Add_customer(Resource):    
    def post(self):
        try:
            c = Customer(name=request.json['name'], username=request.json['username'], password=request.json['password'], level=request.json['level'])
            db.session.add(c)
            db.session.commit()
            return {"message": 'customer created with name '+request.json['name']}, 201
        except:
            return {'message': 'Something went wrong'}

class Login(Resource):    
    def post(self):
        try:
            if session['username']:
                return {"message": 'Already Logged in as '+ session['username']}, 200
        except:
            pass
        try:
            uname = request.json['username']
            pword = request.json['password']
            if Customer.query.filter_by(username=uname).first():
                custom = Customer.query.filter_by(username=uname).first()
                if Customer.query.get(custom.cust_id).password == pword:
                    
                    session['username'] = uname
                    
                    return {"message": 'Successfully Logged in as '+ uname}, 201
                else:
                    return  {"message": 'Incorrect Username or Password'}, 404
            else:
                return  {"message": 'Incorrect Username or Password'}, 404
        except:
                return  {"message": 'Incorrect Username or Password'}, 404

class Logout(Resource):    
    def get(self):      
        session['username'] = None
        return {"message":"User Logged Out"}
    def post(self):      
        session['username'] = None
        return {"message":"User Logged Out"}

class Add_vendor(Resource):
    def post(self):
        try:
            if session['username']:
                pass 
            else:
                return {"message": 'Login Required'}
            data = Vendor(cust_id=request.json['cust_id'], restaurant_name=request.json['restaurant_name'])
            db.session.add(data)
            db.session.commit()
            return {"message": 'Vendor created with restaurant name '+request.json['restaurant_name']}, 201
        except:
            return {'message': 'Something went wrong'}


class Get_all_vendors(Resource):
    def get(self):
        if session['username']:
            pass
        else:
            return {"message": 'Login Required'}

        vendors = Vendor.query.all()
        params = []
        m = 0
        for i in vendors:
            id = i.vendor_id
            vendor_info = {"vendor_id":i.vendor_id, "cust_id":i.cust_id, "restaurant_name":i.restaurant_name, "data":[]}
            params.append(vendor_info)

            res = db.session.query(Food).filter_by(vendor_id=id).all()
            for j in res:
                dict = {"food_id":j.food_id, "vendor_id":j.vendor_id, "dish_name":j.dish_name, "calories_per_gm":j.calories_per_gm, "available_quantity":j.available_quantity, "unit_price":j.unit_price}
                params[m]['data'].append(dict)
            m = m+1
            
        return params, 200

class Add_item(Resource):
    def post(self):
        if session['username']:
            pass 
        else:
            return {"message": 'Login Required'}
        uname = session['username'] 
        cust_info = Customer.query.filter_by(username=uname).first()
        if Vendor.query.filter_by(cust_id=cust_info.cust_id).first():
            food = Food(vendor_id=request.json['vendor_id'], 
                        dish_name=request.json['item_name'], calories_per_gm=request.json['calories_per_gm'],
                        available_quantity=request.json['available_quantity'],unit_price=request.json['unit_price'])
            db.session.add(food)
            db.session.commit()
            return {"message": 'Item added Successfully'}, 200
        else:
            return {"message": 'Don\'t have required privileges'}, 404

class Place_order(Resource):
    def post(self):
        if session['username']:
            pass 
        else:
            return {"message": 'Login Required'}

        try:
            cust_id=request.json['cust_id']
            f_id=request.json['item_id']
            quantity=request.json['quantity']

            item = Food.query.filter_by(food_id=f_id).first()
            if item.available_quantity >= quantity:
                pass
            else:
                return  {"message": 'quantity not available'}, 404
            total = quantity * item.unit_price
            item.available_quantity = item.available_quantity - quantity

            order = Orders(cust_id=cust_id, total_amount=total)
            db.session.add(order)
            db.session.commit()

            last_item = Orders.query.order_by(Orders.order_id.desc()).first()

            orderitems = OrderItems(order_id=last_item.order_id, food_id=f_id, quantity=quantity, amount=total)
            db.session.add(orderitems)
            db.session.commit()
            
            return {"message": 'Order Created Successfully'}, 200
        except:
            return {'message': 'Something went wrong'}


class Get_all_orders_by_customer(Resource):
    def post(self):
        if session['username']:
            pass 
        else:
            return {"message": 'Login Required'}
        id = request.json['cust_id']
        all_orders = db.session.query(Orders).filter_by(cust_id=id).all()
        params = []
        for i in all_orders:
            d = str(i.date)
            params2 = {"order_id":i.order_id, "cust_id":i.cust_id, "total_amount":i.total_amount, "date":d}
            params.append(params2)
        return params, 200

class Get_all_orders(Resource):
    def get(self):
        if session['username']:
            pass 
        else:
            return {"message": 'Login Required'}

        uname = session['username']
        cust_info = Customer.query.filter_by(username=uname).first()
        if cust_info.level == 2:
            all_orders = Orders.query.all()
            params = []
            for i in all_orders:
                d = str(i.date)
                params2 = {"order_id":i.order_id, "cust_id":i.cust_id, "total_amount":i.total_amount, "date":d}
                params.append(params2)
            return params, 200
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

# {
#     "vendor_id": 1,
#     "item_name": "burger",
#     "available_quantity": 5,
#     "calories_per_gm": 22,
#     "unit_price": 20
# }

# {
#     "cust_id":1,
#     "item_id":1,
#     "quantity":2
# }

# {
#     "cust_id": 3
# }