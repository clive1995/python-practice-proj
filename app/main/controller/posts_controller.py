from flask import request
from flask_restplus import Resource
from ..service.constants import *
from ..service.post_service import *
from ..utils.post_dto import PostsDTO
from app.main.utils.middleware.route_guard import roles_required

api = PostsDTO.api


@api.route('/')
class Postapi(Resource):
    @api.doc(security="apikey")
    @roles_required("ADMIN","DEVELOPER")
    @api.expect(PostsDTO.addPost)
    def post(self):
        data = request.json
        return addPost(data=data)

    @api.doc(security="apikey")
    @roles_required("ADMIN","DEVELOPER")
    @api.expect(Userconst.getuserParams)
    @api.marshal_list_with(PostsDTO.getPost)
    def get(self):
        data = Userconst.getuserParams.parse_args()
        return getPost(data=data)

@api.route('/likes')
class Likes(Resource):
    @api.doc(security='apikey')
    @roles_required("ADMIN","DEVELOPER")
    @api.expect(PostsDTO.getLikes)
    def post(self):
        data = request.json
        return addLikes(data=data)

    @api.doc(security='apikey')
    @roles_required('ADMIN','DEVELOPER')
    @api.expect(PostsDTO.getLikes)
    def delete(self):
        data = request.json
        return deleteLike(data=data)


@api.route('/comments')
class Comments(Resource):
    @api.doc(security='apikey')
    @roles_required('ADMIN','DEVELOPER')
    @api.expect(PostsDTO.postComments)
    def post(self):
        data = request.json
        return addComment(data=data)

    @api.doc(security='apikey')
    @roles_required('ADMIN', 'DEVELOPER')
    @api.expect(PostsDTO.deleteComments)
    def delete(self):
        data = request.json
        return deleteComment(data=data)


