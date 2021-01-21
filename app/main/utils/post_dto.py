from flask_restplus import Namespace,fields
from ..service.constants import *
class PostsDTO:
    api = Namespace('Posts',authorizations=Const.authorizations,description="Post related API's")

    addPost = api.model('addPost',{
        "text":fields.String(),
        "name":fields.String(),
    })

    getLikes = api.model('getLikes',{
        "userId":fields.String()
    })

    # getComments = api.model("getComments",{
    #     user
    #     text
    #     createdOn
    # })
    userInfo = api.model("userInfo",{
        "name": fields.String(),
        "email": fields.String(),
        "publicId": fields.String()
    })
    getindividualComment = api.model('getindividualComment',{
        'publicId':fields.String(),
        'text':fields.String(),
        'userInfo':fields.List(fields.Nested(userInfo))
    })
    getPost = api.model('getPost',{
        "publicId":fields.String(),
        "text":fields.String(),
        "name":fields.String(),
        "comments":fields.List(fields.Nested(getindividualComment)),
        "likes": fields.List(fields.Nested(userInfo)),
    })

    getPostResponse = api.model('getPostResponse',{
        'status': fields.String(),
        'message': fields.String(),
        'data':fields.Nested(getPost)
    })

    getLikes = api.model('getLikes',{
        # 'publicId':fields.String(),
        'postId':fields.String()
    })

    getOnePost = api.model('getOnePost',{
        'postId':fields.String()
    })

    postComments = api.model('postComments',{
        'postId':fields.String(),
        # 'userId':fields.String(),
        'text':fields.String(),
    })

    deleteComments = api.model('deleteComments',{
        'commentId':fields.String(),
        'postId':fields.String()
    })

    comments = api.model('comments',{
        "publicId":fields.String(),
        "text":fields.String(),
    })

    userInfo = api.model('userInfo',{
        "name": fields.String(),
        "email":  fields.String(),
        "role":  fields.String(),
    })

    commentOutput = api.model('commentOutput',{
        "comments":fields.Nested(comments),
        'userInfo':fields.Nested(userInfo)
    })
    commentPaginate = api.model('commentPaginate',{
        "publicId": fields.String(),
        "text": fields.String(),
        "name": fields.String(),
        "postImage": fields.String(),
        "comments":fields.List(fields.Nested(commentOutput))
    })