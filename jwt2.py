from datetime import datetime
from flask import Flask, json, jsonify, request, make_response
import jwt
import datetime
from functools import wraps

from flask_restful import Resource, Api

app = Flask(**name**)
app.config['SECRET_KEY'] = 'thisisthesecretkey'
api = Api(app)

def token_required(f):
@wraps(f)
def decorated(\*args, \*\*kwargs):
token = request.args.get('token')
if token == None:
return make_response(jsonify({'msg':'token missing'}), 200)

        try:
            output = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            # return make_response(jsonify({'output':output}))
        except:
            return make_response(jsonify({'message':'Token is invalid'}), 403)

        return f(*args, **kwargs)
    return decorated

class ExampleWithAuth(Resource):
@token_required
def get(self):
return jsonify({'message':'this is only available for people with valid token'})

class Login(Resource):
def post(self):
username = request.form.get('username')
password = request.form.get('password')

        if username and password == 'password':
            token = jwt.encode({'user':username, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm="HS256")
            return jsonify({'token' : token})

        return jsonify({'msg':'Please Login to get access !'})

api.add_resource(ExampleWithAuth, '/api/home', methods=["GET"])
api.add_resource(Login, '/api/login', methods=['GET', 'POST'])

if **name** == "**main**":
app.run(debug=True)