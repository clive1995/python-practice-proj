from ..model.user_model import User
import uuid
from ..service.constants import *

def createUser(data):
    try:
        if not data:
            response_data = {
                'status': Const.FAIL,
                'message': Const.USER_FAIL_MESSAGE
            }
            return response_data, Const.SUCCESS_CODE

        check_user = list(User.objects.aggregate(*[{'$match':{'email':data['email']}}]))
        print(check_user)
        del data['confirmpassword']
        User(**data).save()
        print(data)
    except Exception as e:
        response_data = {
            'status':Const.FAIL,
            'message':e
        }
        return response_data, Const.SUCCESS_CODE