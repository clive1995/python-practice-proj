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
    def post(self,**token):
        data = request.json
        data['userId'] = token['publicId']
        return addPost(data=data)

    @api.doc(security="apikey")
    @roles_required("ADMIN","DEVELOPER")
    # @api.expect(Userconst.getuserParams)
    @api.marshal_list_with(PostsDTO.getPostResponse)
    def get(self,**token):
        # data = Userconst.getuserParams.parse_args()
        data = {}
        print(token['publicId'])
        data['publicId'] = token['publicId']
        return getPost(data=data)


@api.route('/getIndividualPost')
class OnePost(Resource):
    @api.doc(security='apikey')
    @roles_required('ADMIN',"DEVELOPER")
    @api.expect(GetOnePost.getPost)
    @api.marshal_list_with(PostsDTO.getPostResponse)
    def get(self,**token):
        data = GetOnePost.getPost.parse_args()
        data['publicId'] = token['publicId']
        print(data)
        return getPosts(data=data)

@api.route('/comment/paginate')
class CommentPagi(Resource):
    @api.expect(paginationComment.doPaginate)
    @api.marshal_list_with(PostsDTO.commentPaginate)
    def get(self):
        data = paginationComment.doPaginate.parse_args()
        return commentPagination(data=data)


@api.route('/likes')
class Likes(Resource):
    @api.doc(security='apikey')
    @roles_required("ADMIN","DEVELOPER")
    @api.expect(PostsDTO.getLikes)
    def post(self,**token):
        data = request.json
        data['publicId'] = token['publicId']
        return addLikes(data=data)

    @api.doc(security='apikey')
    @roles_required('ADMIN','DEVELOPER')
    @api.expect(PostsDTO.getLikes)
    def delete(self,**token):
        data = request.json
        data['publicId'] = token['publicId']
        return deleteLike(data=data)


@api.route('/comments')
class Comments(Resource):
    @api.doc(security='apikey')
    @roles_required('ADMIN','DEVELOPER')
    @api.expect(PostsDTO.postComments)
    def post(self,**token):
        data = request.json
        data['userId'] = token['publicId']
        return addComment(data=data)

    @api.doc(security='apikey')
    @roles_required('ADMIN', 'DEVELOPER')
    @api.expect(PostsDTO.deleteComments)
    def delete(self,**token):
        data = request.json
        data['userId'] = token['publicId']
        return deleteComment(data=data),



