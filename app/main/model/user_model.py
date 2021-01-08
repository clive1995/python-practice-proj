from .. import mdb


class User(mdb.Document):
    publicId = mdb.UUIDField(binary=True)
    name = mdb.StringField()
    email = mdb.EmailField()
    password = mdb.StringField()
    passwordsalt = mdb.StringField()
    profileImage = mdb.StringField()
    createdOn = mdb.DateField()