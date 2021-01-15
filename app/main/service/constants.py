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
    ALLOWED_EXTENSIONS = {'jpg','jpeg','png'}
    APP_ROOT = os.path.dirname(os.path.abspath(__name__))
    # requestParser = reqparse.RequestParser
    # requestParser.parse_args("publicId")

class Userconst:
    getuserParams = reqparse.RequestParser()
    getuserParams.add_argument('publicId',type=str,required=True)

def has_req_format(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in Const.ALLOWED_EXTENSIONS