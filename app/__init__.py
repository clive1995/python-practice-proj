from flask_restplus import Api
from flask import Blueprint
from .main.controller.user_controller import api as user_port

blueprint = Blueprint('api',__name__,url_prefix='/api/v1')

api = Api(blueprint,title='Connect app',version='1.3',description='connection')

api.add_namespace(user_port)