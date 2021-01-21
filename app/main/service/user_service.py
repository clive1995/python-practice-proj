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
                "message":Const.USER_EXISTS_LOGIN_TO_CONTINUE
            }
            return response_data,Const.ERROR_CODE

        if data['confirmpassword'] != data['password']:
            return {
                'status':Const.FAIL,
                'message':Const.MISMATCHED_PASSWORD
            }, Const.ERROR_CODE

        if data['role'].upper() == 'ADMIN':
            return {
                'status':Const.FAIL,
                'message':Const.ADMIN_CAN_ASSIGN_ROLE
            }, Const.ERROR_CODE

        salt = gen_salt()
        data['password'] = generate_password_hash(data['password'],salt)
        data['passwordsalt'] = salt
        del data['confirmpassword']
        data['publicId'] = uuid.uuid4()
        User(**data).save()

        response_data = {
            'status': Const.SUCCESS,
            'message':Const.USER_ADDED_SUCCESSFULLY
        }
        return response_data, Const.SUCCESS_CODE
    except Exception as e:
        response_data = {
            'status':Const.FAIL,
            'message':e.errors
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

        if data['status'].upper() == "ACTIVE":
            data['status'] = True
        else:
            data['status'] = False

        profile ={'profile':data}

        User.objects(publicId=publicId).update(set__profile=profile['profile'])

        response_data = {
            'status': Const.SUCCESS,
            'message':Const.USER_UPDATED_SUCCESSFULLY
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
        if not fetchUser:
            response_data = {
                'status': Const.FAIL,
                'message': Const.USER_DOESNOT_EXISTS
            }
            return response_data, Const.ERROR_CODE

        return {
            "status":Const.SUCCESS,
            'message':"",
            'data':fetchUser[0]['profile']
        }, Const.SUCCESS_CODE

    except Exception as e:
        response_data = {
            'status':Const.FAIL,
            'message':[]
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
        # User.objects(publicId=data['publicId']).update(**fetch_user[0])
        User.objects(publicId=data['publicId']).update(set__profile__experience=fetch_user[0]['profile']['experience'])
        response_data = {
            'status': Const.SUCCESS,
            'message': Const.EXPERIENCE_UPDATED
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
        User.objects(publicId=data['publicId']).update(add_to_set__profile__experience=data['experience'])
        response_data = {
            'status': Const.SUCCESS,
            'message': Const.EXPERIENCE_ADDED
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


        return {'status':Const.SUCCESS,
                'message':'',
                'data':fetch_user[0]['profile']['experience']
                }, Const.SUCCESS_CODE
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

        fetch_user = User.objects.aggregate(*[
            {
                '$match':{
                    'publicId':uuid.UUID(data['userPublicId'])
                }
            },
            {
                '$project':{
                    'profile':{
                        'experience': {
                            '$filter': {
                                'input': '$profile.experience',
                                'as': 'expor',
                                'cond': {'$eq': ['$$expor.publicId', uuid.UUID(data['experiencePublicId'])] }
                            }
                        }
                    }
                }
            }
        ])
        fetch_user = list(fetch_user)
        if not fetch_user:
            response_object = {
                'status':Const.FAIL,
                'message':Const.USER_DOESNOT_EXISTS
            }
            return response_object, Const.ERROR_CODE

        User.objects(publicId=data['userPublicId']).update(pull__profile__experience__publicId=uuid.UUID(data['experiencePublicId']))

        response_data = {
            'status': Const.SUCCESS,
            'message':Const.EXPERIENCE_DALETED
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

        fetch_education = filter(lambda x:x['publicId']==uuid.UUID(data['education']['publicId']), fetch_user[0]['profile']['education'])
        fetch_education = list(fetch_education)

        index = fetch_user[0]['profile']['education'].index(fetch_education[0])
        fetch_user[0]['profile']['education'][index] = data['education']

        User.objects(publicId=data['publicId']).update(set__profile__education=fetch_user[0]['profile']['education'])

        response_data = {
            'status': Const.SUCCESS,
            'message':Const.EDUCATION_UPDATED
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
            "message":Const.EDUCATION_DELETED
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

        data['education']['publicId'] = uuid.uuid4()

        User.objects(publicId=data['publicId']).update(add_to_set__profile__education=data['education'])
        response_data = {
            'status': Const.SUCCESS,
            'message': Const.EDUCATION_ADDED_SUCCESS
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

        fetch_user = User.objects.aggregate(*[
            {'$match':{'publicId':uuid.UUID(data['publicId'])}},
            projected
        ])
        fetch_user = list(fetch_user)

        if not fetch_user:
            response_object = {
                'status':Const.FAIL,
                'message':Const.USER_DOESNOT_EXISTS
            }
            return response_object, Const.FAIL

        return {'status':Const.SUCCESS,
                'message':'',
                'data':fetch_user[0]['profile']['education']
                }, Const.SUCCESS_CODE

    except Exception as e:
        response_data = {
            'status':Const.FAIL,
            'message':e
        }
        return response_data, Const.ERROR_CODE

def login_user(data):
    try:
        fetch_user = User.objects.aggregate(*[{'$match':{'email':data['username']}}])
        fetch_user = list(fetch_user)
        verify = check_password_hash(fetch_user[0]['password'].encode('utf-8') , fetch_user[0]['passwordsalt'],data['password'])
        if not verify:
            response_data = {
                'status':Const.FAIL,
                'message':Const.MISMATCHED_PASSWORD
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
