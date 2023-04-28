"""Holds the application factory and its derivative functions."""
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# Initializes the SQLAlchemy object
db = SQLAlchemy()


def create_app(test_config=None):
    """Creates and configures an instance of the Flask application.

    :param test_config: The test config object.
    :return: The Flask app.
    """

    # Constructs the Flask app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # Loads the instance config object when not testing
        app.config.from_object("config.ProductionConfig")
    else:
        # Loads the test config object if passed in
        app.config.from_mapping(test_config)

    # Initializes the Flask app with the SQLAlchemy object
    db.init_app(app)

    # Registers the blueprints
    register_blueprints(app)

    # Prepares the database and login functionality
    prepare_database_and_login(app)

    return app


def register_blueprints(app):
    """Registers the blueprints of the flaskr package.

    :param app: The Flask app.
    """

    # Imports the blueprint modules from flaskr
    from flaskr import auth, blog

    # Registers the blueprints from the above modules
    app.register_blueprint(auth.bp, url_prefix="/")
    app.register_blueprint(blog.bp, url_prefix="/")


def prepare_database_and_login(app):
    """Prepares the database and login manager.

    :param app: The Flask app.
    """

    # Imports all database models to ensure db.create_all() is going to be
    # called properly
    from flaskr.models import Post, Upvote, User

    # Constructs the app context and database, respectively
    with app.app_context():
        db.create_all()

    # Points the LoginManager instance to the Login Page
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        """Locates the current user of the session by his/her ID.

        :param user_id: The User ID.
        :return: The current user.
        """

        return User.query.get(int(user_id))
