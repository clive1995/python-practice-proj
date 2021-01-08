from .. import mdb
from .user_model import User

class Experience(mdb.embeddedDocument):
    title =  mdb.StringField()
    company =  mdb.StringField()
    location =  mdb.StringField()
    fromdate =  mdb.DateField()
    todate = mdb.DateField()
    current =mdb.BooleanField()
    description = mdb.DateField()


class Education(mdb.Document):
    school = mdb.StringField()
    degree = mdb.StringField()
    fieldofstudy = mdb.StringField()
    fromdate = mdb.DateField()
    todate = mdb.DateField()
    current = mdb.BooleanField()
    description = mdb.StringField()


class Social(mdb.Document):
    youtube = mdb.StringField()
    twitter = mdb.StringField()
    facebook = mdb.StringField()
    linkedin = mdb.StringField()
    instagram = mdb.StringField()


class Profile(mdb.Document):
    publicId = mdb.UUIDField(binary=True)
    userId = mdb.ReferenceField(User)
    company = mdb.StringField()
    website = mdb.StringField()
    location = mdb.StringField()
    status = mdb.StringField()
    skills = mdb.ListField()
    bio = mdb.StringField()
    githubusername = mdb.StringField()
    experience = mdb.ListField(mdb.EmbeddedDocumentField(Experience))
    education = mdb.ListField(mdb.EmbeddedDocumentField(Education))
    social = mdb.embeddedDocument(Social)
    createdOn = mdb.DateField()

