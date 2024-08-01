from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from flask_login import login_required, current_user
from .models import Post, User, Like, Comment, EditUser, FilterForm, SortForm, Apply
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from . import db

views = Blueprint("views", __name__)


## WEBPAGES ##

# HOME ROUTE

@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)


# MENU ROUTE

@views.route("/menu")
def menu():
    return render_template("menu.html", user=current_user, posts=posts)


# NEWS ROUTE

@views.route("/news")
def news():
    return render_template("news.html", user=current_user, posts=posts)


# SETTINGS ROUTE

@views.route("/settings")
@login_required
def settings():
    return render_template("settings.html", user=current_user, posts=posts)


## ACTIONS ##


## ADMIN ROUTES ##

# DASHBOARD ROUTE

@views.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    if not current_user.is_staff:
        flash('You do not have permission to access this page.', category='error')
        return redirect(url_for('views.home'))

    query = User.query

    sort_by = request.args.get('sort_by', 'email_asc')
    sort_form = SortForm(data={'sort_by': sort_by})
    filter_form = FilterForm()

    # SORT USER

    if request.args.get('sort_by'):
        sort_by = request.args.get('sort_by')
        if sort_by == 'email_asc':
            query = query.order_by(User.email.asc())
        elif sort_by == 'email_desc':
            query = query.order_by(User.email.desc())
        # STAFF - [ INVERTED ASC/DESC TO MAKE SENSE ]
        elif sort_by == 'is_staff_asc':
            query = query.order_by(User.is_staff.desc())
        elif sort_by == 'is_staff_desc':
            query = query.order_by(User.is_staff.asc())

    # FILTER USER
    if filter_form.validate_on_submit():
        if filter_form.email.data:
            query = query.filter(User.email.contains(filter_form.email.data))
        if filter_form.is_staff_true.data and not filter_form.is_staff_false.data:
            query = query.filter_by(is_staff=True)
        elif filter_form.is_staff_false.data and not filter_form.is_staff_true.data:
            query = query.filter_by(is_staff=False)

    users = query.all()

    # EDIT USER ROUTE

    edit_user_id = request.args.get('edit_user_id')
    edit_form = EditUser()
    sort_form = SortForm()
    if edit_user_id:
        user = User.query.get_or_404(edit_user_id)

        # Admin Config Lock
        if user.email == 'admin@sanctamaria.school.nz':
            flash('This user cannot be edited.', category='error')
            return redirect(url_for('views.dashboard'))

        # User Email
        if request.method == 'POST':
            if edit_form.validate_on_submit():

                # Existing User Email
                existing_user = User.query.filter_by(
                    email=edit_form.email.data).first()
                if existing_user and existing_user.id != user.id:
                    flash('Email is already in use.', category='error')
                    return render_template("dashboard.html",
                                           user=current_user, users=users, edit_form=edit_form, edit_user_id=edit_user_id,
                                           filter_form=filter_form, sort_form=sort_form)

                # Update User Email

                user.email = edit_form.email.data
                user.is_staff = edit_form.is_staff.data

                # User Password
                if edit_form.password.data or edit_form.confirm_password.data:
                    if edit_form.password.data == edit_form.confirm_password.data:
                        user.password = generate_password_hash(
                            edit_form.password.data)
                    elif edit_form.password.data or edit_form.confirm_password.data:
                        flash('Please confirm password!', category='error')
                        return render_template("dashboard.html",
                                               user=current_user, users=users, edit_form=edit_form, edit_user_id=edit_user_id,
                                               filter_form=filter_form, sort_form=sort_form)
                db.session.commit()
                flash('User configuration successful!', category='success')
                return redirect(url_for('views.dashboard'))
            else:
                flash('Passwords do not match!', category='error')
        else:
            edit_form = EditUser(obj=user)

    return render_template("dashboard.html",
                           user=current_user, users=users, edit_form=edit_form, edit_user_id=edit_user_id,
                           filter_form=filter_form, sort_form=sort_form)


# DELETE USER ROUTE

@views.route('/dashboard/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_staff:
        flash('Access denied!', 'danger')
        return redirect(url_for('views.home'))

    user = User.query.get_or_404(user_id)

    # Admin Config Lock
    if user.email == 'admin@sanctamaria.school.nz':
        flash('This user cannot be deleted.', category='error')
        return redirect(url_for('views.dashboard'))

    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('views.dashboard'))


# WEEK DATES

def get_week_dates(start_date):
    dates = []
    # Beninging of the Week
    start_of_week = start_date - timedelta(days=start_date.weekday())
    for tabledate in range(5):
        day_date = start_of_week + timedelta(days=tabledate)
        dates.append(day_date)
    return dates


# APPLY ROUTE

@views.route("/apply")
@login_required
def apply():
    posts = Apply.query.all()
    post_accept = Apply.query.filter_by(status='accepted').all()
    post_pending = Apply.query.filter_by(status='pending').all()

    # DISPLAY DATE UNDER WEEKDAY
    today = datetime.now()
    week_dates = get_week_dates(today)
    weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    dates_data = {weekday[tabledate]: week_dates[tabledate]
                  for tabledate in range(5)}

    return render_template("apply.html", user=current_user, posts=posts, post_accept=post_accept, post_pending=post_pending, dates=dates_data)


# CREATE APPLICATIONS ROUTE

@views.route("/apply/submit_duty", methods=['GET', 'POST'])
@login_required
def create_dutydate():
    if request.method == "POST":
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        date_duty = request.form.get('date_duty')
        date_day = request.form.get('date_day')
        yearlevel = request.form.get('yearlevel')
        school_id = request.form.get('school_id')

        # Year Level Validation
        if not firstname or not lastname or not yearlevel:
            flash('Full name, date and year level required.', category='error')
        elif yearlevel in ['≤10']:
            flash('Year 10 students or below are unable to apply for duty.',
                  category='error')
        else:
            # Formatting User Apply Input
            post = Apply(
                firstname=firstname, lastname=lastname,
                date_duty=date_duty, date_day=date_day,
                yearlevel=yearlevel, email=current_user.email, author=current_user.id,
                schoolid=current_user.schoolid
            )
            db.session.add(post)
            db.session.commit()
            flash('Successfully applied!', category='success')

            # Store Selected Duty Date
            session['selected_duty_day'] = date_day
            session['selected_duty_week'] = date_duty

            # Redirect to the 'apply' route
            return redirect(url_for('views.apply'))

    return render_template('submitduty.html', user=current_user)


# DELETE PENDING APPLICATIONS

@views.route("/apply/delete-apply/<id>")
@login_required
def delete_duty(id):
    application = Apply.query.filter_by(id=id).first()
    if not application:
        flash('Application does not exist.', category='error')
    elif current_user.id != application.author and not current_user.is_staff:
        flash('You do not have permission to delete this application.',
              category='error')
    else:
        db.session.delete(application)
        db.session.commit()
        flash('Application deleted.', category='success')
        return redirect(url_for('views.apply'))
    return redirect(url_for('views.apply'))


# ACCEPT APPLICATIONS

@views.route("/apply/accept-apply/<int:post_id>", methods=['GET', 'POST'])
@login_required
def accept_application(post_id):
    post = Apply.query.get_or_404(post_id)

    if not current_user.is_staff:
        flash('You do not have permission to do this.', category='error')
        return redirect(url_for('views.apply'))

    post.status = 'accepted'
    db.session.commit()
    flash('Barista added!', category='success')

    return redirect(url_for('views.apply'))


# DELETE ACCEPTED APPLICATIONS

@views.route("/apply/delete-duty/<id>", methods=['POST'])
@login_required
def delete_accept(id):
    application = Apply.query.filter_by(id=id).first()
    if not application:
        flash('Barista does not exist.', category='error')
    elif current_user.id != application.author and not current_user.is_staff:
        flash('You do not have permission to delete this.',
              category='error')
    else:
        db.session.delete(application)
        db.session.commit()
        flash('Barista removed.', category='success')
    return redirect(url_for('views.apply'))


# CREATE POSTS ROUTE

@views.route("/create_post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')
        if not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.blog'))
    return render_template('create_post.html', user=current_user)


# USER POSTS ROUTE

@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))
    posts = Post.query.filter_by(author=user.id).all()
    return render_template("posts.html", user=current_user, posts=posts, username=username)


# DELETE POST

@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash('Post does not exist.', category='error')
    elif post.author != current_user.id:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')
        return redirect(url_for('views.blog'))


# LIKE POST

@views.route("/like-post/<post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(
        author=current_user.id, post_id=post_id).first()

    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})


# CREATE COMMENT

@views.route("/create-comment/<post_id>", methods=["POST"])
@login_required
def create_comment(post_id):
    text = request.form.get('text')
    if not text:
        flash('Comment cannot be empty', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist', category="error")
    return redirect(url_for('views.blog'))


# DELETE COMMENT

@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        flash('Comment does not exist', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('views.blog'))
