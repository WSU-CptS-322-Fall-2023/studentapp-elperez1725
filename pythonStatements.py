

from app import db

from app.models import Student, Class, enrolled
from datetime import datetime
db.create_all()



# import db models
from app.models import Class
from app.models import Major



#create class objects and write them to the database
newClass = Class(coursenum='322', major ="CptS", title="Software Engineering")
db.session.add(newClass)
newClass = Class(coursenum='315', major="CE", title="Fluid Mechanics")
db.session.add(newClass)
db.session.commit()

#Creating major objects
newMajor = Major(name='Cpts', department="School of EECS")
db.session.add(newMajor)
newMajor = Major(name="CE", department="Civil Engineering")
db.session.add(newMajor)
Major.query.all()
for m in Major.query.all():
    print(m)

# query and print classes
Class.query.all()
Class.query.filter_by(coursenum='322').all()
Class.query.filter_by(coursenum='322').first()
myclasses = Class.query.order_by(Class.coursenum.desc()).all()
for c in myclasses:
    print(c.coursenum)
