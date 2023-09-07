from flask import Blueprint, render_template, flash, redirect, url_for
from app import app,db
from datetime import datetime
from app.Controller.auth_forms import RegistrationForm, LoginForm, EditForm, EmptyForm
from app.Model.models import Student
from flask_login import login_user, current_user, logout_user, login_required
from config import Config


auth_blueprint = Blueprint("auth", __name__)
auth_blueprint.template_folder = Config.TEMPLATE_FOLDER


@app.route('/register', methods=['GET', 'POST'])
def register():
    rform = RegistrationForm()
    if rform.validate_on_submit():
        student = Student(username=rform.username.data, email=rform.email.data, firstname=rform.firstname.data, lastname=rform.lastname.data, address=rform.address.data)
        student.set_password(rform.password.data)
        db.session.add(student)
        db.session.commit()
        flash("Congratulations, you are now a registered user!!")
        return redirect(url_for("routes.index"))
    return render_template('register.html',form=rform)




@app.route("/login", methods=["GET", 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("routes.index"))
    lform = LoginForm()
    if lform.validate_on_submit():
        student = Student.query.filter_by(username=lform.username.data).first()
        if (student is None) or (student.check_password(lform.password.data) == False):
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))
        login_user(student, remember = lform.remember_me.data)
        return redirect(url_for("routes.index"))
    return render_template('login.html',title="Sign In", form=lform)

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))