from flask import Blueprint, render_template, flash, redirect, url_for, request
from app import app,db
from datetime import datetime
from app.Controller.forms import ClassForm, RegistrationForm, LoginForm, EditForm, EmptyForm
from app.Model.models import Class, Major, Student
from flask_login import login_user, current_user, logout_user, login_required
from config import Config


routes_blueprint = Blueprint("routes", __name__)
routes_blueprint.template_folder = Config.TEMPLATE_FOLDER


@routes_blueprint.route("/", methods=["GET"])
@routes_blueprint.route("/index", methods=["GET"])


@routes_blueprint.route('/', methods=['GET'])
@routes_blueprint.route('/index', methods=['GET'])
@login_required
def index():
    emptyform = EmptyForm()
    allclasses = Class.query.order_by(Class.major).all()
    return render_template('index.html', title="Course List", classes=allclasses, eform=emptyform)



@routes_blueprint.route('/createclass/', methods=['GET', 'POST'])
@login_required
def createclass():
    form = ClassForm()
    if form.validate_on_submit():
        newClass = Class(coursenum= form.coursenum.data, title=form.title.data, major=form.major.data.name)
        db.session.add(newClass)
        db.session.commit()
        flash("Class " + newClass.major + "-" + newClass.coursenum+ " is created" )
        return redirect(url_for('index'))
    return render_template('create_class.html',form=form)




@routes_blueprint.before_request
def before_requests():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.add(current_user)
        db.session.commit()



@routes_blueprint.route("/display_profile", methods=["GET"])
@login_required
def display_profile():
    emptyform = EmptyForm()
    return render_template("display_profile.html", title="Display Profile", student=current_user, eform=emptyform)


@routes_blueprint.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    eform = EditForm()
    if request.method == "POST":
        if eform.validate_on_submit():
           theuser = Student.query.filter_by(id=current_user.id)
           current_user.firstname = eform.firstname.data
           current_user.lastname = eform.lastname.data
           current_user.address = eform.address.data
           current_user.email = eform.email.data
           current_user.set_password(eform.password.data)
           db.session.add(current_user)
           db.session.commit()
           flash("Your profile has been updated")
           return redirect(url_for("routes.display_profile"))
        
    elif request.method == "GET":
        eform.firstname.data = current_user.firsname
        eform.lastname.data = current_user.lastname
        eform.address.data = current_user.address
        eform.email.data = current_user.email

        pass
    else:
        pass
    return render_template("edit_profile.html", title="Edit Profile", form=eform)

@routes_blueprint.route('/roster/<classid>', methods=["GET"])
@login_required
def roster(classid):
    theclass = Class.query.filter_by(id=classid).first()
    return render_template("roster.html", title="Class Roster", current_class= theclass)

@routes_blueprint.route("/enroll/<classid>", methods=["POST"])
@login_required
def enroll(classid):
    eform = EmptyForm()
    if eform.validate_on_submit():
        theclass = Class.query.filter_by(id=classid).first()
        if theclass is None:
            flash("Class with id {} not found".format(classid))
            return redirect(url_for('routes.index'))
        current_user.enroll(theclass)
        db.session.commit()
        flash("You are now enrolled in class {} {}".format(theclass.major, theclass.coursenum))
    else:
        return redirect(url_for('routes.index'))
    


@routes_blueprint.route("/unenroll/<classid>", methods=["POST"])
@login_required
def unenroll(classid):
    eform = EmptyForm()
    if eform.validate_on_submit():
        theclass = Class.query.filter_by(id=classid).first()
        if theclass is None:
            flash("Class with id {} not found".format(classid))
            return redirect(url_for('routes.index'))
        current_user.unenroll(theclass)
        db.session.commit()
        flash("You are now un-enrolled in class {} {}".format(theclass.major, theclass.coursenum))
    else:
        return redirect(url_for('routes.index'))