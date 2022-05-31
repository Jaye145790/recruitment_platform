from app import app, db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Document, UserMixin):
    meta = {
        "collection": "user",
        "ordering": ["-id"],
        "strict": True
    }
    username = db.StringField()
    password_hash = db.StringField()
    nickname = db.StringField()
    floder = db.StringField()
    superuser = db.BooleanField(default=False)

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)
        self.save()

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Interviewee(db.Document):
    meta = {
        "collection": "interviewee",
        "ordering": ["-id"],
        "strict": True
    }
    name = db.StringField()
    gender = db.StringField()
    school = db.StringField()
    major = db.StringField()
    education = db.StringField()
    graduated = db.StringField()
    experience = db.StringField()
    level = db.StringField()
    resume = db.BooleanField(default=True)
    interview = db.BooleanField(default=True)
    dept = db.StringField(default="")
    thinkTime = db.IntField(default=-1) #-1
    hire = db.BooleanField(default=False)
