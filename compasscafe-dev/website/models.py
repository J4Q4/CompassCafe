# Authentication and Database Models
from sqlalchemy.sql import func
from flask_login import UserMixin
from . import db
# User Admin Handling
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FloatField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Optional, NumberRange

## DATABASE ENTRY CLASSES ##


# USER CLASS

# Regular User

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    schoolid = db.Column(db.Integer, unique=True)
    password = db.Column(db.String(250))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    is_staff = db.Column(db.Boolean, default=False)


# Configure User

class EditUser(FlaskForm):
    email = StringField('Change Email', validators=[
        DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Change Password', render_kw={
                             "placeholder": "Enter New Password"})
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            Optional(), EqualTo('password', message='Passwords must match')],
        render_kw={"placeholder": "Re-Enter New password"})
    is_staff = BooleanField()
    submit = SubmitField('Update User', render_kw={"class": "btn-primary"})


# Filter User

class FilterForm(FlaskForm):
    # User Filter Dashboard
    email = StringField('Email', validators=[Optional()], render_kw={
                        "placeholder": "Email"})
    is_staff_true = BooleanField('Is Admin')
    is_staff_false = BooleanField('Not Admin')
    # Submit Button
    submit = SubmitField('Filter', render_kw={"class": "btn-primary"})


# Sort User

class SortForm(FlaskForm):
    sort_by = SelectField(validators=[Optional()])
    submit = SubmitField('Sort', render_kw={"class": "btn-primary"})


# USER ACTIONS

# User's Application
class Apply(db.Model):
    # Visible Inputs
    firstname = db.Column(db.String(150), nullable=False)
    lastname = db.Column(db.String(150), nullable=False)
    # Week A or B
    date_duty = db.Column(db.String(50), nullable=True)
    # Tuesday or Thursday Lunchtimes
    date_day = db.Column(db.String(50), nullable=True)
    yearlevel = db.Column(db.String(50), nullable=False)
    # Non-visible Inputs
    id = db.Column(db.Integer, primary_key=True)
    schoolid = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(150), db.ForeignKey(
        'user.email', ondelete='CASCADE'), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', foreign_keys=[
                           author], backref='applications')
    # Visibility
    status = db.Column(db.String(50), default='pending')


# Filter Apply

class FilterApply(FlaskForm):
    schoolid = StringField('School ID', validators=[Optional()])
    date_duty = SelectField('Week', validators=[Optional()], render_kw={
                            "class": "apply-selectfilter"})
    date_day = SelectField('Day', validators=[Optional()], render_kw={
                           "class": "apply-selectfilter"})
    yearlevel = SelectField('Year Level', validators=[Optional()], render_kw={
                            "class": "apply-selectfilter"})
    submit = SubmitField('Filter', render_kw={"class": "btn-primary"})


# MENU INTERFACE
class Menu(db.Model):
    # Menu Items
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(150), nullable=True, default='default.jpg')
    item = db.Column(db.String(35), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(50), nullable=False)
    # Non-visible Inputs
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref='menu', lazy=True)


# Edit Menu
class EditMenu(FlaskForm):
    item = StringField('Item Name', validators=[
                       DataRequired()], render_kw={"maxlength": "35"})
    price = FloatField('Price', validators=[
                       DataRequired(), NumberRange(min=0.0)])
    description = TextAreaField('Description', validators=[
                                Optional()], render_kw={"maxlength": "100"})
    category = SelectField('Category', choices=[], validators=[DataRequired()])
    image = FileField('Menu Item Image', validators=[Optional()])


# Filter Menu

class FilterMenu(FlaskForm):
    item = StringField('Item Name', validators=[Optional()])
    submit = SubmitField('Filter', render_kw={"class": "btn-primary"})


# Sort Menu

class SortMenu(FlaskForm):
    sort_by = SelectField('Sort By', validators=[Optional()])
    submit = SubmitField('Sort', render_kw={"class": "btn-primary"})
