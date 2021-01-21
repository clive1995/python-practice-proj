from flask_restplus import reqparse
import os
from flask_jwt_extended import create_access_token
import random
from app.main import bcrypt


def gen_salt():
    salt = str(os.urandom(random.randint(14, 18))).lstrip('b')
    return salt


def generate_password_hash(password, salt):
    hash_pwd = bcrypt.generate_password_hash(salt + password)
    return hash_pwd


def check_password_hash(password_hash,salt,password):
    return bcrypt.check_password_hash(password_hash, salt + password)


def generate_access_token(public_id,role):
    try:
        identity = {
            'publicId':public_id,
            'role':role
        }
        access_token = create_access_token(expires_delta=False,identity=identity)
        return access_token
    except Exception as e:
        return {
            'status':Const.FAIL,
            'message':e
        }, Const.ERROR_CODE

class Const:
    authorizations = {
        'apikey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'X-API-KEY'
        }
    }
    SUCCESS_CODE = 200
    ERROR_CODE = 400
    FAIL="FAIL"
    SUCCESS = "SUCCESS"
    USER_FAIL_MESSAGE="FAILED TO SAVE USER"
    USER_SUCCESS_MESSAGE = "SAVED USER SUCCESSFULLY"
    MISSING_USER_INPUT = "User input missing"
    USER_DOESNOT_EXISTS = "User does not exists"
    USER_EXISTS_LOGIN_TO_CONTINUE = "User already exists, please login to continue"
    MISMATCHED_PASSWORD="'mis-matched password'"
    ADMIN_CAN_ASSIGN_ROLE  = 'Only Admin can assign admin role'
    USER_ADDED_SUCCESSFULLY = "User added Successfully"
    USER_UPDATED_SUCCESSFULLY = "User Updated Successfully"
    EXPERIENCE_ADDED = 'Experience added'
    EXPERIENCE_UPDATED = 'Experience Updated'
    EXPERIENCE_DALETED = 'Experience Deleted'
    EDUCATION_UPDATED = 'Education Updated Successfully'
    EDUCATION_DELETED = "Education Deleted"
    EDUCATION_ADDED_SUCCESS = 'Education added Successfully'
    POST_ADDED = "Post added"
    USER_NOT_FOUND = "user not found"
    NO_DATA_FOUND="no data found"
    COMMENT_DOES_NOT_EXISTS = "comment does not exists"
    YOU_CANNOT_LIKE_YOUR_OWN_POST = 'You cannot like your own post'
    YOU_HAVE_ALREADY_LIKED_THIS_POST = 'You have already liked this post'
    LIKED = "liked"
    SELECT_A_COMMENT_TO_DISLIKE = "select a comment to dislike"
    NOT_LIKED = "you have not liked this post"
    LIKE_REMOVED = 'Your like is removed for this post'
    PROPER_DATA = "enter proper data"
    COMMENT_NOT_FOUND = "Comment not found"
    POST_ADDED = 'Post added Successfully'
    NO_POST_FOUND = 'Post not found'
    POST_DELETED = 'Post deleted Successfully'
    PAGINATION_FAILED = 'pagination failed'
    ALLOWED_EXTENSIONS = {'jpg','jpeg','png'}
    APP_ROOT = os.path.dirname(os.path.abspath(__name__))
    # requestParser = reqparse.RequestParser
    # requestParser.parse_args("publicId")


class Userconst:
    getuserParams = reqparse.RequestParser()
    getuserParams.add_argument('publicId',type=str,required=True)


def has_req_format(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in Const.ALLOWED_EXTENSIONS


class GetOnePost:
    getPost = reqparse.RequestParser()
    getPost.add_argument('postId',type=str,required=True)

class paginationComment:
    doPaginate = reqparse.RequestParser()
    doPaginate.add_argument('postId',type=str,required=True)
    doPaginate.add_argument('pgno', type=str, required=True)
    doPaginate.add_argument('per_page', type=str, required=True)
    doPaginate.add_argument('order', type=str, required=True)