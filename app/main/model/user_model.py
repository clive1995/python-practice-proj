from .. import mdb
from .profile_model import Profile

ROLES = ('CLIENT','DEVELOPER','ADMIN')

class User(mdb.Document):
    publicId = mdb.UUIDField(binary=True)
    name = mdb.StringField()
    email = mdb.EmailField()
    password = mdb.StringField()
    passwordsalt = mdb.StringField()
    profileImage = mdb.StringField(default="")
    createdOn = mdb.DateField()
    role = mdb.StringField(choice=ROLES)
    profile = mdb.EmbeddedDocumentField(Profile, required=True, default=Profile())