from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post, User, Like, Comment
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

# DASHBOARD ROUTE
@views.route("/dashboard")
@login_required
def dashboard():
    if not current_user.is_staff:
        flash('You do not have permission to access this page.', category='error')
        return redirect(url_for('views.home'))
    return render_template("dashboard.html", user=current_user, posts=posts)


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
