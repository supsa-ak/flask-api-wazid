from flask import Flask, jsonify, make_response, request, session
from flask_sqlalchemy import SQLAlchemy
from apispec import APISpec
from flask_restful import Resource, Api
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_session import Session
import json

application = Flask(__name__)
application.secret_key = 'flask-restraunt-1234'
application.config["SESSION_PERMANENT"] = False
application.config["SESSION_TYPE"] = "filesystem"
Session(application)

api = Api(application)  # Flask restful wraps Flask app around it.

application.config.update({
    'APISPEC_SPEC': APISpec(
        title='Flask Restaurant',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
    'API '
})
docs = FlaskApiSpec(application)

@application.errorhandler(404) 
def invalid_route(e): 
    return  {"message": 'Incorrect Path, check your endpoint'}, 404


from app.models import *