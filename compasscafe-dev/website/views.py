from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post, User, Like, Comment, EditUser, FilterForm, SortForm
from werkzeug.security import generate_password_hash
from . import db

views = Blueprint("views", __name__)


## WEBPAGES ##

# HOME ROUTE
@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)

# APPLY ROUTE
@views.route("/apply")
@login_required
def apply():
    return render_template("apply.html", user=current_user, posts=posts)

# MENU ROUTE
@views.route("/menu")
def menu():
    return render_template("menu.html", user=current_user, posts=posts)

# NEWS ROUTE
@views.route("/news")
def news():
    return render_template("news.html", user=current_user, posts=posts)

# CONTACT ROUTE
@views.route("/contact")
@login_required
def contact():
    return render_template("contact.html", user=current_user, posts=posts)

# SETTINGS ROUTE
@views.route("/settings")
@login_required
def settings():
    return render_template("settings.html", user=current_user, posts=posts)




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
        
        if request.method == 'POST':
            if edit_form.validate_on_submit():
                # Update User Email
                user.email = edit_form.email.data
                user.is_staff = edit_form.is_staff.data
                # Update User Password
                if edit_form.password.data == edit_form.confirm_password.data:
                    user.password = generate_password_hash(edit_form.password.data)
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




## ACTIONS ##

# CREATE APPLICATIONS ROUTE
# DELETE APPLICATIONS ROUTE
# CREATE NEWS ROUTE
# EDIT NEWS ROUTE
# DELETE NEWS ROUTE








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