from functools import wraps

from flask import request
from flask_jwt_extended import decode_token


def roles_required(*role_names):
    def wrapper(view_function):
        @wraps(view_function)
        def decorator(*args, **kwargs):
            token = None
            # print(request.headers)
            if 'X-API-KEY' in request.headers:
                token = request.headers['X-API-KEY']
            if not token:
                return {'message': 'Token is missing.'}, 401
            try:
                # print(token)
                info = decode_token(token)
                # print(info)
                role = info['identity']['role']
                # print(role)

                dataset = {
                    'publicId':info['identity']['publicId'],
                    'role':info['identity']['role']
                }
                if role.upper() not in role_names:
                    return {'message': 'Invalid user'}, 401
            except Exception as e:
                return {'message': 'Invalid Token.'}, 401
            return view_function(*args, **dataset)
        return decorator
    return wrapper

