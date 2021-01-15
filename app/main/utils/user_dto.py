from flask_restplus import Namespace,fields
import uuid
from ..service.constants import *

class UserDTO:
    api = Namespace('User',authorizations=Const.authorizations,description='User Operations')

    PostUser = api.model('PostUser',{
        'name' :fields.String(),
        'email' :fields.String(),
        'password':fields.String(),
        'confirmpassword':fields.String(),
        'role':fields.String()
    })

    experience = api.model('experience',{
        'title': fields.String(),
        'company': fields.String(),
        'location': fields.String(),
        'fromDate': fields.DateTime(),
        'toDate': fields.DateTime(),
        'current': fields.Boolean(),
        'description': fields.String(),
    })

    experience = api.model('experience',{
        'title': fields.String(),
        'company': fields.String(),
        'location': fields.String(),
        'fromDate': fields.DateTime(),
        'toDate': fields.DateTime(),
        'current': fields.Boolean(),
        'description': fields.String(),
    })

    social = api.model('social',{
        'youtube': fields.String(),
        'facebook': fields.String(),
        'instagram': fields.String(),
        'twitter': fields.String(),
        'linkedin': fields.String(),
    })

    putUser = api.model('putUser',{
        'company': fields.String(),
        'website': fields.String(),
        'location': fields.String(),
        'bio': fields.String(),
        'status': fields.String(),
        'githubusername': fields.String(),
        'skills': fields.List(fields.String()),
        'social':fields.Nested(social)
    })

    postExperience = api.model('postExperience',{
        'experience':fields.Nested(experience)
    })

    UserGet = api.model('UserGet',{
        'company': fields.String(),
        'website': fields.String(),
        'location': fields.String(),
        'bio': fields.String(),
        'status': fields.String(),
        'githubusername': fields.String(),
        'skills': fields.String(),
        'social': fields.Nested(social),
    })

    UserExperienceGet = api.model('UserExperienceGet',{
        'publicId':fields.String(),
        'title': fields.String(),
        'company': fields.String(),
        'location': fields.String(),
        'fromDate': fields.DateTime(),
        'toDate': fields.DateTime(),
        'current': fields.Boolean(),
        'description': fields.String(),
    })

    putExperience = api.model('putExperience',{
        'experience':fields.Nested(UserExperienceGet)
    })

    education = api.model('education',{
        'school': fields.String(),
        'degree': fields.String(),
        'fieldofstudy': fields.String(),
        'fromDate': fields.String(),
        'toDate': fields.String(),
        'current': fields.String(),
        'description': fields.String()
    })
    putEducation = api.model('putEducation',{
        'education':fields.Nested(education)
    })

    getEducation = api.model('getEducation',{
        'publicId':fields.String(),
        'school': fields.String(),
        'degree': fields.String(),
        'fieldofstudy': fields.String(),
        'fromDate': fields.String(),
        'toDate': fields.String(),
        'current': fields.String(),
        'description': fields.String()
    })

    deleteExperience = api.model('deleteExperience',{
        # 'userPublicId':fields.String(),
        'experiencePublicId':fields.String()
    })

    deleteEducation = api.model('deleteEducation',{
        'eduPublicId':fields.String()
    })

    modifyEducation = api.model('modifyEductaion',{
        'education':fields.Nested(getEducation)
    })

    login = api.model("login",{
        "username":fields.String(),
        'password':fields.String()
    })

