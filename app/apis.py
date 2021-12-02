# from werkzeug.wrappers import request
from app import *

class Add_customer(Resource):    
    def post(self):
        c = Customer(name=request.json['name'], username=request.json['username'], password=request.json['password'], level=request.json['level'])
        db.session.add(c)
        db.session.commit()
        return {"message": 'customer created'}, 201

api.add_resource(Add_customer, '/addcustomer')

class Login(Resource):    
    def post(self):
        uname = request.json['username']
        pword = request.json['password']
        if Customer.query.filter_by(username=uname).first():
            custom = Customer.query.filter_by(username=uname).first()
            if Customer.query.get(custom.cust_id).password == pword:
                print(session)
                session['username'] = uname
                print(session)
            else:
                return  {"message": 'Incorrect Password'}, 200
            return {"message": 'Successfully Logged in as '+ uname}, 201
        else:
            return  {"message": 'Incorrect Username'}, 200

api.add_resource(Login, '/login')




# del session['username']