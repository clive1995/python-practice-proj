from .constants import *
from ..model.user_model import User
from ..model.posts_model import Post
from werkzeug.utils import secure_filename
import uuid
import os


def upload_profile_image(data):
    try:
        if not data:
            response_object = {
                'status':Const.FAIL,
                'message':Const.USER_FAIL_MESSAGE
            }

            return response_object

        fetch_user = User.objects.aggregate(*[
            {
                '$match':{
                    'publicId':uuid.UUID(data['publicId'])
                }
            },
            {
                '$project':{
                    'publicId':1,
                    'profileImage':1
                }
            }
        ])

        fetch_user = list(fetch_user)
        if not fetch_user:
            response_object = {
                'status':Const.FAIL,
                'message':Const.USER_DOESNOT_EXISTS
            }
            return response_object

        if 'profileImage' in fetch_user[0] and fetch_user[0]['profileImage'] is not None and fetch_user[0]['profileImage'].strip():
            os.remove(os.path.join(Const.APP_ROOT+'\\files',fetch_user[0]['profileImage']))

        file_uploaded = data['file1']
        if file_uploaded and has_req_format(file_uploaded.filename):
            filename = secure_filename(file_uploaded.filename)
            unique_filename = data['publicId']+'_'+filename
            print(unique_filename)
            file_uploaded.save(os.path.join(Const.APP_ROOT+'\\files',unique_filename))
            User.objects(publicId=data['publicId']).update(set__profileImage=unique_filename)

            response_object = {
                'status':Const.SUCCESS,
                'message':'Image uplaoded Successfully'
            }
            return response_object
    except Exception as e:
        response= {
            'status':Const.SUCCESS,
            'message':e
        }
        return response

def uplaod_post_image(data):
    try:
        if not data:
            response_data = {
                'status':Const.SUCCESS,
                'message':Const.USER_FAIL_MESSAGE
            }
            return response_data

        fetch_user = Post.objects.aggregate(*[
            {
                '$match':{
                    'publicId':uuid.UUID(data['publicId'])
                }
            },
            {
                '$project':{
                    'publicId':1,
                    'postImage':1
                }
            }])

        fetch_user = list(fetch_user)
        print(fetch_user)
        if not fetch_user:
            response_data = {
                'status':Const.FAIL,
                'message':'Post not found.'
            }
            return response_data

        if 'postImage' in fetch_user[0] and fetch_user[0]['postImage'].strip() is not None and fetch_user[0]['postImage'].strip():
            if os.path.isfile(os.path.join(Const.APP_ROOT+'\\files', fetch_user[0]['postImage'])):
                os.remove(os.path.join(Const.APP_ROOT+'\\files', fetch_user[0]['postImage']))

        file = data['file1']

        if file and has_req_format(file.filename):
            filename = secure_filename(file.filename)
            uniquename = data['publicId']+'_'+filename
            file.save(os.path.join(Const.APP_ROOT+'\\files',uniquename))
            Post.objects(publicId=data['publicId']).update(set__postImage=uniquename)
            response_data = {
                'status':Const.SUCCESS,
                'message':'Post image saved successfully'
            }
            return response_data, Const.SUCCESS_CODE
        else:
            response_data = {
                'status': Const.FAIL,
                'message': 'failed to save post image'
            }
            return response_data, Const.ERROR_CODE

    except Exception as e:
        response= {
            'status':Const.SUCCESS,
            'message':e
        }
        return response