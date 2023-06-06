from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
# To manage the login related things
from flask_login import LoginManager

# define database connection
db = SQLAlchemy()
DB_NAME = "flask_notes_app_db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'QWERTYUIOPASDFGHJKL'

    # To tell flask where will be the db located.
    # For sqlite database
    # This will store the database in the website directory.
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # To initialize the database for the app.
    db.init_app(app)

    # To import the blueprints.
    # To tell flask abouts the blueprints containing views or url for application.
    from .views import views
    from .auth import auth

    # To register the blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # To create the database.
    from .models import User, Note
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # To tell the flask how to load the user.
    @login_manager.user_loader
    def load_user(user_id):
        # by default, it gets the id
        return User.query.get(int(user_id))

    return app


# Function to create the database if not exists
def create_database(app):
    with app.app_context():
        if not path.exists('website/' + DB_NAME):
            db.create_all()
            print('Created Database!')
