from flask_restplus import Namespace,fields
from ..service.constants import *
from ..service.constants import *
class PostsDTO:
    api = Namespace('Posts',authorizations=Const.authorizations,description="Post related API's")

    addPost = api.model('addPost',{
        "userId":fields.String(),
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

    getPost = api.model('getPost',{
        "publicId":fields.String(),
        "text":fields.String(),
        "name":fields.String(),
        "userInfo": fields.Nested(userInfo),
        "likes": fields.Integer()
    })

    getLikes = api.model('getLikes',{
        'publicId':fields.String(),
        'commentId':fields.String()
    })

    postComments = api.model('postComments',{
        'commentId':fields.String(),
        'userId':fields.String(),
        'text':fields.String(),
    })

    deleteComments = api.model('deleteComments',{
        'commentId':fields.String(),
        'userId':fields.String()
    })