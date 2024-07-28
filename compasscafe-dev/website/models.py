# Authentication and Database Models
from sqlalchemy.sql import func
from flask_login import UserMixin
from . import db
# User Admin Handling
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Optional

## DATABASE ENTRY CLASSES ##


# USER CLASS

# Regular User

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    schoolid = db.Column(db.Integer, unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    is_staff = db.Column(db.Boolean, default=False)


# Configure User

class EditUser(FlaskForm):
    email = StringField('Change Email', validators=[
        DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Change Password', render_kw={"placeholder": "Enter New Password"})
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            Optional(), EqualTo('password', message='Passwords must match')], 
        render_kw={"placeholder": "Re-Enter New password"})
    is_staff = BooleanField()
    submit = SubmitField('Update User', render_kw={"class": "btn btn-primary"})


# Filter User

class FilterForm(FlaskForm):
    email = StringField('Email', validators=[Optional()], render_kw={"placeholder": "Email"})
    is_staff_true = BooleanField('Is Admin')
    is_staff_false = BooleanField('Not Admin')
    submit = SubmitField('Filter', render_kw={"class": "btn btn-primary"})


# Sort User

class SortForm(FlaskForm):
    sort_by = SelectField(
        choices=[
            ('email_asc', 'Email (Ascending)'),
            ('email_desc', 'Email (Descending)'),
            ('is_staff_asc', 'Admin Status (Ascending)'),
            ('is_staff_desc', 'Admin Status (Descending)')
        ],
        validators=[Optional()]
    )
    submit = SubmitField('Sort', render_kw={"class": "btn btn-primary"})


# USER ACTIONS

# User's Post
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    likes = db.relationship('Like', backref='post', passive_deletes=True)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)


# User's Likes

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete='CASCADE'), nullable=False)


# User's Comments

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete='CASCADE'), nullable=False)
