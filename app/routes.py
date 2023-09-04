from flask import render_template, flash, redirect, url_for, request
from app import app,db
from datetime import datetime
from app.forms import ClassForm, RegistrationForm, LoginForm, EditForm
from app.models import Class, Major, Student
from flask_login import login_user, current_user, logout_user, login_required


@app.before_request
def initDB(*args, **kwargs):
    if app.got_first_request:
        db.create_all()
 

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@login_required
def index():
    allclasses = Class.query.order_by(Class.major).all()
    return render_template('index.html', title="Course List", classes=allclasses)



@app.route('/createclass/', methods=['GET', 'POST'])
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    rform = RegistrationForm()
    if rform.validate_on_submit():
        student = Student(username=rform.username.data, email=rform.email.data, firstname=rform.firstname.data, lastname=rform.lastname.data, address=rform.address.data)
        student.set_password(rform.password.data)
        db.session.add(student)
        db.session.commit()
        flash("Congratulations, you are now a registered user!!")
        return redirect(url_for("index"))
    return render_template('register.html',form=rform)


@app.before_request
def before_requests():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.add(current_user)
        db.session.commit()

@app.route("/login", methods=["GET", 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    lform = LoginForm()
    if lform.validate_on_submit():
        student = Student.query.filter_by(username=lform.username.data).first()
        if (student is None) or (student.check_password(lform.password.data) == False):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(student, remember = lform.remember_me.data)
        return redirect(url_for("index"))
    return render_template('login.html',title="Sign In", form=lform)

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/display_profile", methods=["GET"])
@login_required
def display_profile():
    return render_template("display_profile.html", title="Display Profile", student=current_user)


@app.route("/edit_profile", methods=["GET", "POST"])
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
           return redirect(url_for("display_profile"))
        
    elif request.method == "GET":
        eform.firstname.data = current_user.firsname
        eform.lastname.data = current_user.lastname
        eform.address.data = current_user.address
        eform.email.data = current_user.email

        pass
    else:
        pass
    return render_template("edit_profile.html", title="Edit Profile", form=eform)

@app.route('/roster/<classid>', methods=["GET"])
def roster(classid):
    theclass = Class.query.filter_by(id=classid).first()
    return render_template("roster.html", title="Class Roster", current_class= theclass)