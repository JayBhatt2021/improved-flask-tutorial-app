"""Holds the auth blueprint."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr import db
from flaskr.models import User

# The blueprint name is "auth".
# The package that this blueprint is located in is "__name__".
bp = Blueprint("auth", __name__)


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Registers the user if a valid username and password are inputted.

    :return: The rendered HTML of the signed-in version of the Index Template
             if all inputs are valid; otherwise, the rendered HTML of the
             Register Template is returned.
    """

    if request.method == "POST":
        # Gets the inputted username and password from the Register Template
        username = request.form["username"]
        password = request.form["password"]

        # Initializes the error-checking variables
        error = None
        username_exists = User.query.filter_by(username=username).first()

        # Assigns the appropriate message to error (if needed)
        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif username_exists:
            error = "This username already exists."

        # Registers the new user and redirects him/her to the signed-in version
        # of the Index Template if error is None
        if error is None:
            new_user = User(
                username=username,
                password=generate_password_hash(password, method="sha256"),
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("You have been registered!", category="success")

            return redirect(url_for("blog.index"))

        # Flashes an error message if error is not None
        flash(error, category="error")

    return render_template("auth/register.html", user=current_user)


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Logs in the user if the correct username and password are inputted.

    :return: The rendered HTML of the signed-in version of the Index Template
             if all inputs are valid; otherwise, the rendered HTML of the Login
             Template is returned.
    """

    if request.method == "POST":
        # Gets the inputted username and password from the Login Template
        username = request.form["username"]
        password = request.form["password"]

        # Queries the database for the user by the inputted username
        user = User.query.filter_by(username=username).first()

        # Initializes the error-checking variable
        error = None

        # Assigns the appropriate message to error (if needed)
        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif user is None:
            error = "This username does not exist."
        elif not check_password_hash(user.password, password):
            error = "This password is incorrect."

        # Log ins the user if the correct username and password are inputted
        if error is None:
            login_user(user, remember=True)
            flash("You have been logged in!", category="success")

            return redirect(url_for("blog.index"))

        # Flashes an error message if error is not None
        flash(error, category="error")

    return render_template("auth/login.html", user=current_user)


@bp.route("/logout")
@login_required
def logout():
    """Logs out the user to the unsigned-in version of the Index Template if
    he/she was already logged-in.

    :return: The rendered HTML of the unsigned-in version of the Index
             Template.
    """

    logout_user()
    flash("You have been logged out!", category="success")

    return redirect(url_for("blog.index"))
