from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint("auth", __name__)


## USER AUTHENTICATION  WEBPAGES ##

# LOGIN ROUTE

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            # Admin User Login
            if email == 'admin@sanctamaria.school.nz' and check_password_hash('hashed_password', password):
                user.is_staff = True
                db.session.commit()  # Save the changes to the database
                flash('Logged in as admin!', category='success')
            else:
                flash('Logged in successfully!', category='success')

            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        else:
            flash('Incorrect email or password.', category='error')

    return render_template("login.html", user=current_user)


# SIGN UP ROUTE

@auth.route("/signup", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        schoolid = request.form.get("schoolid")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()
        schoolid_exists = User.query.filter_by(schoolid=schoolid).first()

        if email_exists:
            flash('Email is already in use.', category='error')
        elif schoolid_exists:
            flash('School ID is already in use.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match!', category='error')
        elif schoolid and len(schoolid) < 5:
            flash('School ID is too short.', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters.', category='error')
        elif len(email) < 4:
            flash('Email is invalid', category='error')
        else:
            new_user = User(email=email, schoolid=schoolid, password=generate_password_hash(
                password1, method='scrypt:32768:8:1'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)


# LOGOUT ROUTE

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash('User logged out!', category='success')
    return redirect(url_for("views.home"))
