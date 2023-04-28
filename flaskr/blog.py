"""Holds the blog blueprint."""
from flask import (Blueprint, flash, jsonify, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_required

from flaskr import db
from flaskr.models import Post, Upvote

# The blueprint name is "blog".
# The package that this blueprint is located in is "__name__".
bp = Blueprint("blog", __name__)


@bp.route("/")
@bp.route("/index")
def index():
    """Shows the Index Template with all posts.

    :return: The rendered HTML of the Index Template.
    """

    posts = Post.query.all()

    return render_template("blog/index.html", user=current_user, posts=posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Creates a new post for the current user.

    :return: The rendered HTML of the signed-in version of the Index Template
             if all inputs are valid; otherwise, the rendered HTML of the
             Create Template is returned.
    """

    if request.method == "POST":
        # Gets the inputted title and body from the Create Template
        title = request.form["title"]
        body = request.form["body"]

        # Initializes the error-checking variable
        error = None

        # Assigns the appropriate message to error (if needed)
        if not title:
            error = "Title is required."
        elif not body:
            error = "The post cannot be empty."

        # Creates a new post and redirects the user to the signed-in version of
        # the Index Template if error is None; otherwise, an error message is
        # flashed.
        if error is not None:
            flash(error, category="error")
        else:
            created_post = Post(
                title=title,
                body=body,
                author_id=current_user.id
            )
            db.session.add(created_post)
            db.session.commit()
            flash("Your post has been created!", category="success")

            return redirect(url_for("blog.index"))

    return render_template("blog/create.html", user=current_user)


@bp.route("/update/<int:post_id>", methods=("GET", "POST"))
@login_required
def update(post_id):
    """Updates a post if the current user is the author.

    :param post_id: The Post ID.
    :return: The rendered HTML of the signed-in version of the Index Template
             if all inputs are valid; otherwise, the rendered HTML of the
             Update Template is returned.
    """

    # Queries the database for the post by post_id
    post = Post.query.filter_by(id=post_id).first()

    if request.method == "POST":
        # Gets the inputted title and body from the Update Template
        title = request.form["title"]
        body = request.form["body"]

        # Initializes the error-checking variable
        error = None

        # Assigns the appropriate message to error (if needed)
        if not title:
            error = "Title is required."
        elif not body:
            error = "The post cannot be empty."

        # Updates the post and redirects the user to the signed-in version of
        # the Index Template if error is None; otherwise, an error message is
        # flashed.
        if error is not None:
            flash(error, category="error")
        else:
            post.title = title
            post.body = body
            db.session.commit()
            flash("Your post has been updated!", category="success")

            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", user=current_user, post=post)


@bp.route("/delete/<int:post_id>", methods=("POST",))
@login_required
def delete(post_id):
    """Deletes a post after ensuring that the post exists and the logged-in
    user is the author of the post.

    :param post_id: The Post ID.
    :return: The rendered HTML of the signed-in version of the Index Template.
    """

    # Queries the database for the post by post_id
    post = Post.query.filter_by(id=post_id).first()

    # Deletes the post and redirects the user to the signed-in version of the
    # Index Template
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!.", category="success")

    return redirect(url_for("blog.index"))


@bp.route("/upvote/<int:post_id>", methods=("POST",))
@login_required
def upvote(post_id):
    """Increments the upvote counter for a post by 1 if its upvote button is
    selected.

    Only decrements the upvote counter for that post by 1 if its upvote button
    was previously selected AND is deselected.

    :param post_id: The Post ID.
    :return: A JSON object containing the number of upvotes the post has and
             whether the post has been upvoted by the user."""

    # Queries the database for the post by post_id
    post = Post.query.filter_by(id=id).first()

    # Queries the database for the upvote by upvoter_id and upvoted_post_id
    upvote = Upvote.query.filter_by(
        upvoter_id=current_user.id, upvoted_post_id=post_id
    ).first()

    if upvote:
        # Decrements the upvote counter for the post by 1
        db.session.delete(upvote)
        db.session.commit()
    else:
        # Increments the upvote counter for the post by 1
        upvote = Upvote(upvoter_id=current_user.id, upvoted_post_id=post_id)
        db.session.add(upvote)
        db.session.commit()

    return jsonify(
        {
            "upvotes": len(post.upvotes),
            "upvoted": current_user.id
            in map(lambda upvoter: upvoter.upvoter_id, post.upvotes),
        }
    )
