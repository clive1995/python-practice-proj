from flask_restplus import Resource
from ..utils.user_dto import UserDTO
from flask import request
from ..service.user_service import *
from app.main.utils.middleware.route_guard import roles_required
api =UserDTO.api

@api.route('/')
class UserOperations(Resource):
    @api.expect(UserDTO.PostUser)
    def post(self):
        data = request.json
        return createUser(data=data)

    @api.doc(security='apikey')
    @roles_required('ADMIN',"DEVELOPER")
    @api.expect(UserDTO.putUser)
    def put(self,**token):
        data = request.json
        data['publicId'] = token['publicId']
        # data['role'] = token['role']
        return editUser(data=data)

    @api.doc(security='apikey')
    @roles_required('ADMIN',"DEVELOPER")
    # @api.expect(Userconst.getuserParams)
    @api.marshal_list_with(UserDTO.UserGet)
    def get(self, **token):
        data = {}
        data['publicId'] = token['publicId']
        data['role'] = token['role']
        print(data)
        return getUserProfile(data=data)

@api.route('/education')
class Education(Resource):
    @api.doc(security='apikey')
    @roles_required('ADMIN',"DEVELOPER")
    @api.expect(UserDTO.putEducation)
    def post(self,**token):
        data = request.json
        data['publicId']= token['publicId']
        return postEducation(data=data)

    @api.doc(security='apikey')
    @roles_required('ADMIN',"DEVELOPER")
    # @api.expect(Userconst.getuserParams)
    @api.marshal_list_with(UserDTO.getEducation)
    def get(self,**token):
        data = {}
        data['publicId'] = token['publicId']
        return getEducation(data=data)

    @api.doc(security='apikey')
    @roles_required('ADMIN',"DEVELOPER")
    @api.expect(UserDTO.modifyEducation)
    def put(self,**token):
        data = request.json
        data['publicId'] = token['publicId']
        return putEducation(data=data)

    @api.doc(security='apikey')
    @roles_required('ADMIN',"DEVELOPER")
    @api.expect(UserDTO.deleteEducation)
    def delete(self,**token):
        data = request.json
        data['userPublicId'] = token['publicId']
        return deleteEducation(data=data)


@api.route('/experience')
class UserExperience(Resource):
    @api.doc(security='apikey')
    @roles_required('ADMIN', "DEVELOPER")
    @api.expect(UserDTO.putExperience)
    def put(self,**token):
        data = request.json
        data['publicId'] = token['publicId']
        return putExperience(data=data)

    @api.doc(security='apikey')
    @roles_required('ADMIN', "DEVELOPER")
    # @api.expect(Userconst.getuserParams)
    @api.marshal_list_with(UserDTO.UserExperienceGet)
    def get(self,**token):
        # data = Userconst.getuserParams.parse_args()
        data = {}
        data['publicId'] = token['publicId']
        return getUserExperience(data=data)

    @api.doc(security='apikey')
    @roles_required('ADMIN', "DEVELOPER")
    @api.expect(UserDTO.deleteExperience)
    def delete(self,**token):
        ''' delete User Experience
        '''
        data = request.json
        data['userPublicId'] = token['publicId']
        return deleteExperience(data=data)

    @api.doc(security='apikey')
    @roles_required('ADMIN', "DEVELOPER")
    @api.expect(UserDTO.postExperience)
    def post(self,**token):
        data = request.json
        data['publicId'] = token['publicId']
        return postExperience(data=data)

@api.route('/login')
class Login(Resource):
    @api.expect(UserDTO.login)
    def post(self):
        data = request.json
        return login_user(data=data)



