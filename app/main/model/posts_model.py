from .. import mdb
from .user_model import User
import datetime


class Likes(mdb.EmbeddedDocument):
    userId = mdb.ReferenceField(User)


class Comments(mdb.EmbeddedDocument):
    userId = mdb.ReferenceField(User)
    text = mdb.StringField()
    # name = mdb.StringField()
    createdOn = mdb.DateField(default=datetime.datetime.now())


class Post(mdb.Document):
    userId = mdb.ReferenceField(User)
    publicId = mdb.UUIDField()
    text = mdb.StringField()
    name = mdb.StringField(default="")
    postImage = mdb.StringField(default="")
    likes = mdb.ListField(mdb.EmbeddedDocumentField(Likes))
    comments = mdb.ListField(mdb.EmbeddedDocumentField(Comments))
    createdOn = mdb.DateField(default=datetime.datetime.now())