from flask import render_template, flash, redirect, url_for, request
from app import app,db

from app.forms import ClassForm
from app.models import Class, Major



@app.before_request
def initDB(*args, **kwargs):
    if app.got_first_request:
        db.create_all()
 

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    allclasses = Class.query.order_by(Class.major).all()
    return render_template('index.html', title="Course List", classes=allclasses)



@app.route('/createclass/', methods=['GET', 'POST'])
def createclass():
    form = ClassForm()
    if form.validate_on_submit():
        newClass = Class(coursenum= form.coursenum.data, title=form.title.data, major=form.major.data.name)
        db.session.add(newClass)
        db.session.commit()
        flash("Class " + newClass.major + "-" + newClass.coursenum+ " is created" )
        return redirect(url_for('index'))
    return render_template('create_class.html',form=form)