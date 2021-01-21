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
            'response':Const.POST_ADDED
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
                "message":Const.USER_NOT_FOUND
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
                '$lookup':{
                    'from':'user',
                    'localField':'likes.userId',
                    'foreignField':'_id',
                    'as':'likes'
                }
            },
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
                    # "likes": {'$size':'$likes'},
                    "likes":{
                        "name":1,
                        "email":1,
                        "publicId":1
                    }
                }
            }

        ])
        fetch_posts = list(fetch_posts)
        print(fetch_posts)
        # print(fetch_posts)
        # if len(fetch_posts) >0:
        #     # response_data = {
        #     #     "status": Const.SUCCESS,
        #     #     'data': fetch_posts
        #     # }
        #     return fetch_posts, Const.SUCCESS_CODE
        # else:
        #     response_data = {
        #         "status": Const.SUCCESS,
        #         'response': Const.NO_DATA_FOUND
        #     }

        response_data = {
            "status": Const.SUCCESS,
            "message":'',
            'data': fetch_posts
        }
        return response_data, Const.SUCCESS_CODE

    except Exception as e:
        response_data = {
            "status":Const.FAIL,
            "message":e
        }
        return response_data


def addLikes(data):
    try:
        if not data:
            response_data = {
                'status': Const.FAIL,
                'message': Const.USER_DOESNOT_EXISTS
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
                    'publicId':1
                }
            }
        ])

        fetch_user = list(fetch_user)
        if not len(fetch_user):
            response_data = {
                'status':Const.FAIL,
                'message':Const.USER_NOT_FOUND
            }
            return response_data, Const.FAIL

        fetch_comment = Post.objects.aggregate(*[
            {
                '$match':{
                    'publicId':uuid.UUID(data['postId'])
                }
            },
            {
                "$project": {
                    '_id':1,
                    'publicId': 1,
                    'likes': {
                        '$filter': {
                            'input':'$likes',
                            'as': 'like',
                            'cond':{'$eq':['$$like.userId',fetch_user[0]['_id']]}
                        }
                    }
                }
            }
        ])

        fetch_comment = list(fetch_comment)
        # print(fetch_comment[0])
        if not len(fetch_comment):
            response_data = {
                'status':Const.FAIL,
                'message':Const.COMMENT_DOES_NOT_EXISTS
            }
            return response_data, Const.ERROR_CODE
        if fetch_user[0]['_id'] == fetch_comment[0]['_id']:
            response_data = {
                'status':Const.FAIL,
                'message':Const.YOU_CANNOT_LIKE_YOUR_OWN_POST
            }
            return response_data,Const.ERROR_CODE

        if len(fetch_comment[0]['likes']) > 0:
            response_data = {
                'status':Const.SUCCESS,
                'message':Const.YOU_HAVE_ALREADY_LIKED_THIS_POST
            }
            return response_data, Const.SUCCESS_CODE
        new_like = {'userId': fetch_user[0]['_id']}
        Post.objects(publicId=data['postId']).update(add_to_set__likes=new_like)

        # Post.objects(publicId=data['commentId']).update(**fetch_comment[0])

        response_data = {
            'status':Const.SUCCESS,
            'message':Const.LIKED
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
                "message":Const.SELECT_A_COMMENT_TO_DISLIKE
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
                "message":Const.NOT_LIKED
            }
            return response_data
        print(check_like)

        Post.objects(publicId=data['commentId']).update(pull__likes__userId=fetch_user[0]['_id'])

        response_data = {
            'status':Const.SUCCESS,
            'message':Const.LIKE_REMOVED
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
                'message':Const.PROPER_DATA
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
                'message':Const.USER_NOT_FOUND
            }
            return response_data, Const.ERROR_CODE

        fetch_comment = Post.objects.aggregate(*[
            {
                '$match':{
                    'publicId':uuid.UUID(data['postId'])
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
                'message':Const.COMMENT_NOT_FOUND
            }
            return response_data, Const.ERROR_CODE

        Post.objects(publicId=data['postId']).update(add_to_set__comments={'publicId':uuid.uuid4(),'userId':fetch_user[0]['_id'], 'text':data['text'], 'createdOn':datetime.datetime.now()})

        response_data = {
            'status': Const.SUCCESS,
            'message': Const.POST_ADDED
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
                'message':Const.PROPER_DATA
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
                'message':Const.USER_NOT_FOUND
            }
            return response_data, Const.ERROR_CODE

        fetch_comment = Post.objects.aggregate(*[
            {
                '$match':{
                    'publicId':uuid.UUID(data['postId'])
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
                'message':Const.NO_POST_FOUND
            }
            return response_data, Const.ERROR_CODE

        print(fetch_user[0]['_id'])
        Post.objects(publicId=data['postId']).update(pull__comments__publicId=data['commentId'])

        response_data = {
            'status': Const.SUCCESS,
            'message':Const.POST_DELETED
        }
        return response_data, Const.SUCCESS_CODE

    except Exception as e:
        response_data = {
            'status':Const.FAIL,
            'message':e
        }
        return response_data

def getPosts(data):
    try:
        if not data:
            response_data = {
                'status':Const.FAIL,
                'message':Const.PROPER_DATA
            }
            return response_data,Const.ERROR_CODE

        fetch_posts = Post.objects.aggregate(*[
            {'$match':
                 {
                     'publicId':uuid.UUID(data['postId'])
                 }
            },
            {
                '$lookup':{
                    'from':'user',
                    'localField':'likes.userId',
                    'foreignField':'_id',
                    'as':'likeUserInfo'
                }
            },
            {
                '$unwind': {
                    'path': '$comments',
                    'preserveNullAndEmptyArrays': True
                }
            },
            {
              '$lookup':{
                  'from':'user',
                  'localField':'comments.userId',
                  'foreignField':'_id',
                  'as':'userInfo'
              }
            },
            {'$unwind':{
                'path': '$userInfo',
                'preserveNullAndEmptyArrays': True
            }},
            {
                '$group':{
                    '_id':'$_id',
                    'text':{'$first':'$text'},
                    'name':{'$first':'$name'},
                    'publicId':{'$first':'$publicId'},
                    'likes':{'$first':'$likeUserInfo'},
                    'comments':{'$push':{'userId':'$comments.userId','publicId':'$comments.publicId','text':'$comments.text','userInfo':'$userInfo'}}
                }
            },
            {'$project':
                 {
                     'publicId':1,
                     'text': 1,
                     'name':1,
                     'likes':{
                         'publicId': 1,
                         '_id': 1,
                         'name': 1,
                         'email': 1,
                     },
                     'comments':{
                         'userId':1,
                         'publicId':1,
                         'text':1,
                         'userInfo': {
                             'publicId': 1,
                             '_id': 1,
                             'name': 1,
                             'email': 1,
                         }
                     },
                 }
            },
        ])
        fetch_posts = list(fetch_posts)
        print(fetch_posts)
        # fetch_posts[0]['comments']=[]
        if len(fetch_posts):
            if 'publicId' not in fetch_posts[0]['comments'][0]:
                fetch_posts[0]['comments'] =[]
        else:
            fetch_posts=[]
        return {'status':Const.SUCCESS,'message':'','data':fetch_posts}, Const.SUCCESS_CODE
    except Exception as e:
        response_data = {
            'status':Const.FAIL,
            'message':e
        }
        return response_data,Const.ERROR_CODE


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

        fetch_user = User.objects.aggregate(*[{'$match': {'publicId': uuid.UUID(data['publicId'])}}])
        fetch_user = list(fetch_user)
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
                'response': Const.NO_DATA_FOUND
            }
            return response_data, Const.SUCCESS_CODE
    except Exception as e:
        response_data = {
            "status": Const.FAIL,
            "message": e
        }
        return response_data


def commentPagination(data):
    try:
        if not data:
            response_data = {
                'statue':Const.FAIL,
                'message':Const.PAGINATION_FAILED
            }
            return response_data, Const.ERROR_CODE

        page_no = int(data['pgno'])
        per_page = int(data['per_page'])
        order = data['order']

        if page_no > 1:
            offset = (page_no - 1)* per_page
        else:
            offset = page_no * per_page

        if order == 'asc':
            sort = 1
        else:
            sort = -1
        get_post = Post.objects.aggregate(*[
            {
                '$match':{'publicId':uuid.UUID(data['postId'])},
            },
            {
                '$project':{
                    'publicId':1,
                    'name':1,
                    'text':1,
                    'postImage':1
                }
            }
        ])
        get_post  = list(get_post)
        get_comments =  Post.objects.aggregate(*[
            {
                '$match':{
                    'publicId':uuid.UUID(data['postId'])
                }
            },
            {
                '$project':{
                    'text':1,
                    'name':1,
                    'comments': 1
                }
            },
            {
                "$unwind":"$comments"
            },
            {
                '$lookup':{
                    'from':'user',
                    'localField':'comments.userId',
                    'foreignField':'_id',
                    'as':'userInfo'

                }
            },
            { '$unwind':'$userInfo'},
            {
              '$skip':  offset
            },
            {
              '$limit':per_page
            },
            {
                '$sort':{'comments.text':sort}
            },
            {
                '$project':{
                    'comments':{
                        'text':1,
                        'publicId':1,
                    },
                    'userInfo':{
                        'name':1,
                        'email':1,
                        'role':1
                    }
                }
            }
        ])

        get_comments = list(get_comments)

        final_output = {}
        final_output['publicId'] = get_post[0]['publicId']
        final_output['text'] = get_post[0]['text']
        final_output['name'] = get_post[0]['name']
        final_output['postImage'] = get_post[0]['postImage']
        final_output['comments'] = get_comments

        return final_output
    except Exception as e:
        response_data = {
            'status':Const.FAIL,
            'message':e
        }

        return response_data, Const.ERROR_CODE



