from ..model.posts_model import Post
from ..model.user_model import User
from .constants import *
import uuid
import datetime

def addPost(data):
    try:
        if not data:
            response_object = {
                'status':Const.FAIL,
                'message':Const.USER_FAIL_MESSAGE
            }
            return response_object, Const.ERROR_CODE


        fetch_user = User.objects.aggregate(*[{'$match':{'publicId':uuid.UUID(data['userId'])}}])
        fetch_user = list(fetch_user)
        data['userId'] = fetch_user[0]['_id']
        data['publicId'] = uuid.uuid4()
        Post(**data).save()
        response_data = {
            "status":Const.SUCCESS,
            'response':"Post added"
        }
        return response_data, Const.SUCCESS_CODE
    except Exception as e:
        response_data = {
            "status":Const.FAIL,
            "message":e
        }
        return response_data

def getPost(data):
    try:
        if not data:
            response_data = {
                "status": Const.FAIL,
                "message": Const.USER_FAIL_MESSAGE
            }
            return response_data

        fetch_user = User.objects.aggregate(*[
            {
                "$match":{
                    "publicId":uuid.UUID(data['publicId'])
                }
            },
            {
                "$project":{
                    "_id":1
                }
            }
        ])

        if not fetch_user:
            response_data = {
                "status":Const.FAIL,
                "message":"user not found"
            }
            return response_data, Const.ERROR_CODE
        fetch_user = list(fetch_user)
        print(fetch_user)
        print(fetch_user[0]['_id'])
        fetch_posts = Post.objects.aggregate(*[
            {
                "$match":{
                    "userId":fetch_user[0]['_id']
                }
            },
            {
                '$lookup':{
                    'from':'user',
                    'localField':'userId',
                    'foreignField':'_id',
                    'as':'userInfo'
                }
            },
            {'$unwind':'$userInfo'},
            {
                '$project':{
                    "publicId": 1,
                    "text": 1,
                    "name": 1,
                    "userInfo":{
                        "name":1,
                        "email":1,
                        "publicId":1
                    },
                    "likes": {'$size':'$likes'},
                }
            }

        ])
        fetch_posts = list(fetch_posts)
        print(fetch_posts)
        if len(fetch_posts) >0:
            # response_data = {
            #     "status": Const.SUCCESS,
            #     'data': fetch_posts
            # }
            return fetch_posts, Const.SUCCESS_CODE
        else:
            response_data = {
                "status": Const.SUCCESS,
                'response': 'no data found'
            }
            return response_data, Const.SUCCESS_CODE
    except Exception as e:
        response_data = {
            "status":Const.FAIL,
            "message":e
        }
        return response_data


def getUserPost(data):
    try:
        if not data:
            response_data = {
                "status": Const.FAIL,
                "message": Const.USER_FAIL_MESSAGE
            }
            return response_data

        look_up = {
            '$lookup': {
                'from': 'user',
                'localField': 'userId',
                'foreignField': '_id',
                # 'pipeline':[{'$project':{'name':1,'email':1,'profileImage':1}}],
                'as': 'userInfo'
            }
        }

        # projected = {'$project':{
        #     'publicId':1,
        #     'text':1,
        #     'name':1,
        #     'likes':{
        #
        #     }
        # }}
        fetch_user = User.objects.aggregate(*[{'$match': {'publicId': uuid.UUID(data['publicId'])}}])
        fetch_user = list(fetch_user)
        # print(fetch_user)
        print("i am ahere")
        fetch_posts = Post.objects.aggregate(*[
            {'$match': {'userId': fetch_user[0]['_id']}},
            {
                '$lookup': {
                    'from': 'user',
                    'localField': 'userId',
                    'foreignField': '_id',
                    'as': 'userinfo'
                }
            },
            {'$unwind': '$userinfo'},
            {'$unwind': '$likes'},
            {
                '$lookup': {
                    'from': 'user',
                    'localField': 'likes.userId',
                    'foreignField': '_id',
                    'as': 'likedInfo'
                }
            },
            {'$unwind': '$likedInfo'},
            {
                '$group': {
                    "_id": "$_id",
                    "publicId": {"$first": "$publicId"},
                    "text": {"$first": "$text"},
                    "name": {"$first": "$name"},
                    "userId": {"$first": "$userId"},
                    "user": {"$first": "$userinfo"},
                    "comments": {"$first": "$comments"},
                    'likes': {'$push': '$likedInfo'},
                    # 'totalikes':{'$sum':'likes'}
                }
            },
            {
                '$project': {
                    "publicId": 1,
                    "text": 1,
                    "userId": 1,
                    "comments": 1,
                    "user": {
                        'publicId': 1,
                        'name': 1,
                        'email': 1,
                        'profileImage': 1,
                    },
                    'likes': {
                        'publicId': 1,
                        'name': 1,
                        'email': 1,
                        'profileImage': 1,
                    },
                    'totalikes': {'$size': '$likes'},
                }
            }
        ])
        fetch_posts = list(fetch_posts)
        print(fetch_posts)
        if len(fetch_posts) > 0:
            # response_data = {
            #     "status": Const.SUCCESS,
            #     'data': fetch_posts
            # }
            return fetch_posts, Const.SUCCESS_CODE
        else:
            response_data = {
                "status": Const.SUCCESS,
                'response': 'no data found'
            }
            return response_data, Const.SUCCESS_CODE
    except Exception as e:
        response_data = {
            "status": Const.FAIL,
            "message": e
        }
        return response_data



def addLikes(data):
    try:
        if not data:
            response_data = {
                'status': Const.FAIL,
                'message': "please enter a user id"
            }
            return response_data, Const.ERROR_CODE

        fetch_user = User.objects.aggregate(*[
            {
                '$match':{
                    'publicId':uuid.UUID(data['publicId'])
                }
            },
            {
                '$project':{
                    '_id':1,
                }
            }
        ])

        fetch_user = list(fetch_user)
        if not len(fetch_user):
            response_data = {
                'status':Const.FAIL,
                'message':"user not found"
            }
            return response_data, Const.FAIL

        fetch_comment = Post.objects.aggregate(*[{'$match':{'publicId':uuid.UUID(data['commentId'])}},{"$project":{'publicId':1}}])

        fetch_comment = list(fetch_comment)
        if not len(fetch_comment):
            response_data = {
                'status':Const.FAIL,
                'message':'comment does not exists'
            }
            return response_data, Const.ERROR_CODE

        # chec_existing_like = filter(lambda x:x['userId'] == fetch_user[0]['_id'],fetch_comment[0]['likes'])
        chec_existing_like = Post.objects.aggregate(*[{
            "$match":{
                'publicId':uuid.UUID(data['commentId']),
                'likes.userId':fetch_user[0]['_id']
            }
        }])

        chec_existing_like = list(chec_existing_like)
        if len(chec_existing_like) > 0:
            response_data = {
                'status':Const.SUCCESS,
                'message':'You have already liked this post'
            }
            return response_data, Const.SUCCESS_CODE

        new_like = {'userId': fetch_user[0]['_id']}
        Post.objects(publicId=data['commentId']).update(add_to_set__likes=new_like)

        # Post.objects(publicId=data['commentId']).update(**fetch_comment[0])

        response_data = {
            'status':Const.SUCCESS,
            'message':"liked"
        }

        return response_data, Const.SUCCESS

    except Exception as e:
        response_data = {
            'status':Const.FAIL,
            'message':e
        }
        return response_data, Const.ERROR_CODE


def deleteLike(data):
    try:
        if not data:
            return_data = {
                "status":Const.FAIL,
                "message":"select a comment to dislike"
            }
            return return_data, Const.ERROR_CODE

        fetch_user = User.objects.aggregate(*[{'$match':{'publicId':uuid.UUID(data['publicId'])}},{'$project':{'_id':1}}])

        fetch_user = list(fetch_user)
        if not len(fetch_user):
            response_data = {
                "status":Const.FAIL,
                "message":Const.USER_DOESNOT_EXISTS
            }
            return response_data, Const.ERROR_CODE

        check_like = Post.objects.aggregate(*[{
            '$match':{
                'publicId':uuid.UUID(data['commentId']),
                'likes.userId':fetch_user[0]['_id']
            }
        }])
        check_like = list(check_like)
        if not len(check_like):
            response_data = {
                "status":Const.SUCCESS,
                "message":"you have not liked this post"
            }
            return response_data
        print(check_like)

        Post.objects(publicId=data['commentId']).update(pull__likes__userId=fetch_user[0]['_id'])

        response_data = {
            'status':Const.SUCCESS,
            'message':'Your like is removed for this post'
        }

        return response_data, Const.SUCCESS_CODE
        # Post.objects(publicId=data['commentId']).update(unset__likes__userId=fetch_user[0]['_id'])

    except Exception as e:
        response_data = {
            'status':Const.FAIL,
            'message':e
        }
        return response_data, Const.ERROR_CODE

def addComment(data):
    try:
        if not data:
            response_data = {
                'status':Const.FAIL,
                'message':'enter proper data'
            }
            return response_data, Const.ERROR_CODE

        fetch_user = User.objects.aggregate(*[
            {
                '$match':{
                    'publicId':uuid.UUID(data['userId'])
                },
            },
            {
                '$project':{
                    '_id':1
                }
            }
        ])

        fetch_user = list(fetch_user)
        if not len(fetch_user):
            response_data = {
                'status':Const.FAIL,
                'message':'user not found'
            }
            return response_data, Const.ERROR_CODE

        fetch_comment = Post.objects.aggregate(*[
            {
                '$match':{
                    'publicId':uuid.UUID(data['commentId'])
                }
            },
            {
                '$project':{
                    '_id':1
                }
            }
        ])

        fetch_comment = list(fetch_comment)
        if not len(fetch_comment):
            response_data = {
                'status':Const.FAIL,
                'message':'Comment not found'
            }
            return response_data, Const.ERROR_CODE

        Post.objects(publicId=data['commentId']).update(add_to_set__comments={'userId':fetch_user[0]['_id'], 'text':data['text'], 'createdOn':datetime.datetime.now()})

        response_data = {
            'status': Const.SUCCESS,
            'message': 'Post added Successfully'
        }
        return response_data, Const.SUCCESS_CODE

    except Exception as e:
        response_data = {
            'status':Const.FAIL,
            'message':e
        }
        return response_data


def deleteComment(data):
    try:
        if not data:
            response_data = {
                'status':Const.FAIL,
                'message':'enter proper data'
            }
            return response_data, Const.ERROR_CODE

        fetch_user = User.objects.aggregate(*[
            {
                '$match':{
                    'publicId':uuid.UUID(data['userId'])
                }
            },
            {
                '$project':{
                    '_id':1
                }
            }
        ])

        fetch_user = list(fetch_user)
        if not len(fetch_user):
            response_data = {
                'status':Const.FAIL,
                'message':'user not found'
            }
            return response_data, Const.ERROR_CODE

        fetch_comment = Post.objects.aggregate(*[
            {
                '$match':{
                    'publicId':uuid.UUID(data['commentId'])
                }
            },
            {
                '$project':{
                    '_id':1
                }
            }
        ])

        fetch_comment = list(fetch_comment)
        if not len(fetch_comment):
            response_data = {
                'status':Const.FAIL,
                'message':'Comment not found'
            }
            return response_data, Const.ERROR_CODE

        print(fetch_user[0]['_id'])
        Post.objects(publicId=data['commentId']).update(pull__comments__userId=fetch_user[0]['_id'])

        response_data = {
            'status': Const.SUCCESS,
            'message': 'Post deleted Successfully'
        }
        return response_data, Const.SUCCESS_CODE

    except Exception as e:
        response_data = {
            'status':Const.FAIL,
            'message':e
        }
        return response_data