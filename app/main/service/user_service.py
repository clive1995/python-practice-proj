from ..model.user_model import User
from ..model.profile_model import Profile
import uuid
from ..service.constants import *

def createUser(data):
    try:
        if not data:
            response_data = {
                'status': Const.FAIL,
                'message':Const.MISSING_USER_INPUT
            }
            return response_data, Const.ERROR_CODE

        check_user = list(User.objects.aggregate(*[{'$match':{'email':data['email']}}]))
        if check_user:
            response_data = {
                "status":Const.FAIL,
                "message":"User already exists, please login to continue"
            }
            return response_data,Const.ERROR_CODE

        if data['confirmpassword'] != data['password']:
            return {
                'status':Const.FAIL,
                'message':'mis-matched password'
            }, Const.ERROR_CODE

        if data['role'].upper() == 'ADMIN':
            return {
                'status':Const.FAIL,
                'message':'Only Admin can assign admin role'
            }, Const.ERROR_CODE

        salt = gen_salt()
        data['password'] = generate_password_hash(data['password'],salt)
        data['passwordsalt'] = salt
        del data['confirmpassword']
        data['publicId'] = uuid.uuid4()
        User(**data).save()

        response_data = {
            'status': Const.SUCCESS,
            'message':"User added Successfully"
        }
        return response_data, Const.SUCCESS_CODE
    except Exception as e:
        response_data = {
            'status':Const.FAIL,
            'message':e
        }
        return response_data, Const.ERROR_CODE


def editUser(data):
    try:
        if not data:
            response_data = {
                'status': Const.FAIL,
                'message': Const.MISSING_USER_INPUT
            }
            return response_data, Const.ERROR_CODE
        print(data)
        check_user = User.objects.aggregate(*[
            {'$match':{'publicId':uuid.UUID(data['publicId'])}
        }])

        if not check_user:
            response_data = {
                'status': Const.FAIL,
                'message': Const.USER_DOESNOT_EXISTS
            }
            return response_data, Const.ERROR_CODE

        publicId = data['publicId']
        del data['publicId']
        print(data)
        profile ={'profile':data}


        User.objects(publicId=publicId).update(**profile)

        response_data = {
            'status': Const.SUCCESS,
            'message':"User Updated Successfully"
        }
        return response_data, Const.SUCCESS_CODE

    except Exception as e:
        response_data = {
            'status':Const.FAIL,
            'message':e
        }
        return response_data, Const.ERROR_CODE


def getUserProfile(data):
    try:
        if not data:
            response_data = {
                'status': Const.FAIL,
                'message': Const.MISSING_USER_INPUT
            }
            return response_data, Const.ERROR_CODE
        projected = {'$project': {
                "profile": {
                    'company':1,
                    'website':1,
                    'location':1,
                    'status':1,
                    'skills':1,
                    'bio':1,
                    'githubusername':1,
                    'social':{
                        'youtube':1,
                        'twitter':1,
                        'facebook':1,
                        'linkedin':1,
                        'instagram':1
                    },
                }
            }
        }
        fetchUser = User.objects.aggregate(*[
            {
                "$match":{
                    'publicId':uuid.UUID(data['publicId'])
                }
            }
            ,projected])
        fetchUser = list(fetchUser)
        print(fetchUser[0]['profile'])
        if not fetchUser:
            response_data = {
                'status': Const.FAIL,
                'message': Const.USER_DOESNOT_EXISTS
            }
            return response_data, Const.ERROR_CODE

        # response_data = {
        #     'status': Const.SUCCESS_CODE,
        #     'data': fetchUser[0]
        # }
        return fetchUser[0]['profile']

    except Exception as e:
        response_data = {
            'status':Const.FAIL,
            'message':e
        }
        return response_data, Const.ERROR_CODE


def putExperience(data):
    try:
        if not data:
            response_data = {
                'status': Const.FAIL,
                'message': Const.MISSING_USER_INPUT
            }
            return response_data, Const.ERROR_CODE

        fetch_user = User.objects.aggregate(*[
            {'$match':{'publicId':uuid.UUID(data['publicId'])}}
        ])
        if not fetch_user:
            response_data = {
                'status': Const.FAIL,
                'message': Const.USER_DOESNOT_EXISTS
            }
            return response_data, Const.ERROR_CODE

        fetch_user = list(fetch_user)

        del fetch_user[0]['_id']
        filo = filter(lambda exp:exp['publicId'] == uuid.UUID(data['experience']['publicId']),fetch_user[0]['profile']['experience'])

        index = fetch_user[0]['profile']['experience'].index(list(filo)[0])
        fetch_user[0]['profile']['experience'][index] = data['experience']
        User.objects(publicId=data['publicId']).update(**fetch_user[0])
        response_data = {
            'status': Const.SUCCESS,
            'message': 'Experience added'
        }
        return response_data, Const.SUCCESS_CODE
    except Exception as e:
        response_data = {
            'status':Const.FAIL,
            'message':e
        }
        return response_data, Const.ERROR_CODE


def postExperience(data):
    try:
        if not data:
            response_data = {
                'status': Const.FAIL,
                'message': Const.MISSING_USER_INPUT
            }
            return response_data, Const.ERROR_CODE

        fetch_user = User.objects.aggregate(*[{'$match':{'publicId':uuid.UUID(data['publicId'])}}])
        if not fetch_user:
            response_data = {
                'status': Const.FAIL,
                'message': Const.USER_DOESNOT_EXISTS
            }
            return response_data, Const.ERROR_CODE
        fetch_user = list(fetch_user)
        data['experience']['publicId'] = uuid.uuid4()
        fetch_user[0]['profile']['experience'].append(data['experience'])
        del fetch_user[0]['_id']
        User.objects(publicId=data['publicId']).update(**fetch_user[0])
        response_data = {
            'status': Const.SUCCESS,
            'message': 'Experience added'
        }
        return response_data, Const.SUCCESS_CODE
    except Exception as e:
        response_data = {
            'status':Const.FAIL,
            'message':e
        }
        return response_data, Const.ERROR_CODE

def getUserExperience(data):
    try:
        if not data:
            response_data = {
                'status': Const.FAIL,
                'message': Const.MISSING_USER_INPUT
            }
            return response_data, Const.ERROR_CODE

        projected = {
            '$project':{
                'profile':{
                    'experience':{
                        'publicId':1,
                        'title': 1,
                        'company': 1,
                        'location': 1,
                        'fromDate': 1,
                        'toDate': 1,
                        'current': 1,
                        'description': 1,
                    }
                }
            }
        }
        fetch_user = User.objects.aggregate(*[
            {'$match':{'publicId':uuid.UUID(data['publicId'])}},
            projected
        ])

        if not fetch_user:
            response_data = {
                'status': Const.FAIL,
                'message': Const.USER_DOESNOT_EXISTS
            }
            return response_data, Const.ERROR_CODE

        fetch_user = list(fetch_user)
        print(fetch_user[0]['profile']['experience'])
        return fetch_user[0]['profile']['experience']
    except Exception as e:
        response_data = {
            'status':Const.FAIL,
            'message':e
        }
        return response_data, Const.ERROR_CODE


def deleteExperience(data):
    try:
        if not data:
            response_data = {
                'status': Const.FAIL,
                'message': Const.MISSING_USER_INPUT
            }
            return response_data, Const.ERROR_CODE

        fetch_user = User.objects.aggregate(*[{'$match':{'publicId':uuid.UUID(data['userPublicId'])}}])
        if not fetch_user:
            response_object = {
                'status':Const.FAIL,
                'message':Const.USER_DOESNOT_EXISTS
            }
            return response_object, Const.ERROR_CODE

        fetch_user = list(fetch_user)
        fetch_modify = filter(lambda exp:exp['publicId'] != uuid.UUID(data['experiencePublicId']), fetch_user[0]['profile']['experience'])
        fetch_user[0]['profile']['experience'] = fetch_modify
        del fetch_user[0]['_id']
        User.objects(publicId=data['userPublicId']).update(**fetch_user[0])

        response_data = {
            'status': Const.SUCCESS,
            'message': 'Experience Deleted'
        }
        return response_data, Const.SUCCESS_CODE
    except Exception as e:
        response_data ={
            'status':Const.FAIL,
            'message':e
        }
        return response_data,Const.ERROR_CODE


def putEducation(data):
    try:
        if not data:
            response_data = {
                'status':Const.SUCCESS,
                'message':Const.MISSING_USER_INPUT
            }
            return response_data, Const.FAIL

        fetch_user = User.objects.aggregate(*[{'$match':{'publicId':uuid.UUID(data['publicId'])}}])
        fetch_user = list(fetch_user)

        for i in range(0,len(fetch_user[0]['profile']['education'])):
            if fetch_user[0]['profile']['education'][i]['publicId'] == uuid.UUID(data['education']['publicId']):
                index = fetch_user[0]['profile']['education'].index(fetch_user[0]['profile']['education'][i])
                fetch_user[0]['profile']['education'][index] = data['education']

        del fetch_user[0]['_id']
        User.objects(publicId=data['publicId']).update(**fetch_user[0])

        response_data = {
            'status': Const.SUCCESS,
            'message': 'Education Updated Successfully'
        }
        return response_data

    except Exception as e:
        response_data = {
            'status':Const.FAIL,
            'message':e
        }
        return response_data, Const.ERROR_CODE

def deleteEducation(data):
    try:
        if not data:
            response_data = {
                'status':Const.SUCCESS,
                'message':Const.MISSING_USER_INPUT
            }
            return response_data, Const.FAIL
        fetch_user = User.objects.aggregate(*[
            {'$match':{'publicId':uuid.UUID(data['userPublicId'])}}
        ])
        if not fetch_user:
            response_object = {
                'status':Const.FAIL,
                'message':Const.USER_DOESNOT_EXISTS
            }
            return response_object, Const.ERROR_CODE
        fetch_user = list(fetch_user)

        # fetch_user[0]['profile']['education'] = filter(lambda Edu:Edu['publicId'] != data['eduPublicId'], fetch_user[0]['profile']['education'])
        # print(list(fetch_user[0]['profile']['education']))
        del fetch_user[0]['_id']
        User.objects(publicId=data['userPublicId']).update(pull__profile__education__publicId=data['eduPublicId'])

        return_object = {
            "status":Const.SUCCESS,
            "message":"Education Deleted"
        }

        return return_object,Const.SUCCESS_CODE

    except Exception as e:
        response_data = {
            'status':Const.FAIL,
            'message':e
        }
        return response_data, Const.ERROR_CODE

def postEducation(data):
    try:
        if not data:
            response_data = {
                'status':Const.SUCCESS,
                'message':Const.MISSING_USER_INPUT
            }
            return response_data, Const.FAIL

        fetch_user = User.objects.aggregate(*[
            {'$match':{'publicId':uuid.UUID(data['publicId'])}}
        ])

        fetch_user = list(fetch_user)
        # print(data)
        data['education']['publicId'] = uuid.uuid4()
        print(data['education'])
        fetch_user[0]['profile']['education'].append(data['education'])
        print(fetch_user[0]['profile']['education'])
        del fetch_user[0]['_id']
        # print(fetch_user)

        User.objects(publicId=data['publicId']).update(**fetch_user[0])
        response_data = {
            'status': Const.SUCCESS,
            'message': 'Education added Successfully'
        }
        return response_data
    except Exception as e:
        response_data = {
            'status':Const.FAIL,
            'message':e
        }
        return response_data, Const.FAIL

def getEducation(data):
    try:
        if not data:
            response_data = {
                'status':Const.SUCCESS,
                'message':Const.MISSING_USER_INPUT
            }
            return response_data, Const.FAIL

        projected = {'$project':{
            'profile':{
                'education':{
                    'publicId':1,
                    'school':1,
                    'degree':1,
                    'fieldofstudy':1,
                    'fromDate':1,
                    'toDate':1,
                    'current':1,
                    'description':1
                    }
                }
            }
        }
        print(data)
        fetch_user = User.objects.aggregate(*[
            {'$match':{'publicId':uuid.UUID(data['publicId'])}},
            projected
        ])
        fetch_user = list(fetch_user)
        print(fetch_user)

        if not fetch_user:
            response_object = {
                'status':Const.FAIL,
                'message':Const.USER_DOESNOT_EXISTS
            }
            return response_object, Const.FAIL

        return fetch_user[0]['profile']['education']

    except Exception as e:
        response_data = {
            'status':Const.FAIL,
            'message':e
        }
        return response_data, Const.ERROR_CODE

def login_user(data):
    try:
        print(data)
        # fetch_user = User.objects.aggregate(*[{'$match':{'email':data['username']}}])

        fetch_user = User.objects.aggregate(*[{'$match':{'email':data['username']}}])
        print(data['password'].encode('utf-8'))
        fetch_user = list(fetch_user)
        print(fetch_user)
        verify = check_password_hash(fetch_user[0]['password'].encode('utf-8') , fetch_user[0]['passwordsalt'],data['password'])
        if not verify:
            response_data = {
                'status':Const.FAIL,
                'message':'mismatch password'
            }
            return response_data, Const.SUCCESS_CODE
        response_data = {
            'status':Const.SUCCESS,
            'message':generate_access_token(fetch_user[0]['publicId'],fetch_user[0]['role'])
        }
        return response_data
    except Exception as e:
        response_data = {
            'status':Const.FAIL,
            'message':e
        }
        return response_data, Const.ERROR_CODE
