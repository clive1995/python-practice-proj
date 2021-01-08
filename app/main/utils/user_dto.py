from flask_restplus import Namespace,fields


class UserDTO:
    api = Namespace('User',description='User Operations')

    PostUser = api.model('PostUser',{
        'name' :fields.String(),
        'email' :fields.String(),
        'password':fields.String(),
        'confirmpassword':fields.String(),
        'profileImage' :fields.String(),
    })

