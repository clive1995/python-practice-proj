from flask_restplus import Resource
from ..utils.user_dto import UserDTO
from flask import request
from ..service.user_service import *

api =UserDTO.api

@api.route('/')
class UserOperations(Resource):
    @api.expect(UserDTO.PostUser)
    def post(self):
        data = request.json
        return createUser(data=data)