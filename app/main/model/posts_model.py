from .. import mdb
from .user_model import User


class Likes(mdb.Document):
    userId:mdb.ReferenceField(User)


class Comments(mdb.Document):
    user = mdb.StringField()
    text = mdb.StringField()
    name = mdb.StringField()
    createdOn = mdb.DateField()


class Post(mdb.Document):
    userId = mdb.ReferenceField(User)
    text = mdb.StringField()
    name = mdb.StringField()
    likes = mdb.ListField(mdb.EmbeddedDocumentField(Likes))
    comments = mdb.ListField(mdb.EmbeddedDocumentField(Comments))
    createdOn = mdb.DateField()