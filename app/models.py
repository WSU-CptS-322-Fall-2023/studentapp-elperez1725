from app import db
from enum import unique
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coursenum = db.Column(db.String(3))  
    title = db.Column(db.String(150))
    major = db.Column(db.String, db.ForeignKey("major.name"))
    def __repr__(self):
        return '<Class id: {} - coursenum: {}, title: {}, major: {}>'.format(self.id,self.coursenum, self.title, self.major)

    def getTitle(self):
        return self.title 

class Major(db.Model):
    name = db.Column(db.String(), primary_key=True)
    department = db.Column(db.String(150))
    classes = db.relationship("Class", backref="coursemajor", lazy="dynamic")

    def __repr__(self):
        return "<Major name: {} - department: {}>".format(self.name, self.department)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    address = db.Column(db.String(200))
    email = db.Column(db.String(120), unique=True, index=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Student {} - {} {} - {};>'.format(self.id, self.firstname, self.lastname, self.email)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)