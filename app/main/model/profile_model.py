from .. import mdb
import datetime

class Experience(mdb.EmbeddedDocument):
    publicId = mdb.UUIDField()
    title =  mdb.StringField()
    company =  mdb.StringField()
    location =  mdb.StringField()
    fromDate =  mdb.DateField()
    toDate = mdb.DateField()
    current =mdb.BooleanField()
    description = mdb.StringField()


class Education(mdb.EmbeddedDocument):
    publicId = mdb.UUIDField()
    school = mdb.StringField()
    degree = mdb.StringField()
    fieldofstudy = mdb.StringField()
    fromDate = mdb.DateField()
    toDate = mdb.DateField()
    current = mdb.BooleanField()
    description = mdb.StringField()


class Social(mdb.EmbeddedDocument):
    youtube = mdb.StringField()
    twitter = mdb.StringField()
    facebook = mdb.StringField()
    linkedin = mdb.StringField()
    instagram = mdb.StringField()


class Profile(mdb.EmbeddedDocument):
    company = mdb.StringField(required=True, default='')
    website = mdb.StringField(required=True, default='')
    location = mdb.StringField(required=True, default='')
    status = mdb.BooleanField(required=True, default=True)
    skills = mdb.ListField()
    bio = mdb.StringField(required=True, default='')
    githubusername = mdb.StringField(required=True, default='')
    experience = mdb.ListField(mdb.EmbeddedDocumentField(Experience))
    education = mdb.ListField(mdb.EmbeddedDocumentField(Education))
    social = mdb.EmbeddedDocumentField(Social)
    createdOn = mdb.DateField(default=datetime.datetime.now())

