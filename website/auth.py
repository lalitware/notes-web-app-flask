from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


# define login route
# by passing methods list we are permitting the route to handel the given request types.
# By default, it can accept only get request.
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # request.form will have access to the data submitted in the form
    # data = request.form

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # To query the details of the first user having the email
        user = User.query.filter_by(email=email).first()
        # If user with the given email exist.
        if user:
            # To check for the correct password
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                # To log in the user and to crate a session into the flask web server
                # remember = true to remember the session in the browser memory.
                login_user(user, remember=True)
                # Pointing to the home function of views.py
                # Redirect to the home page.
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password!', category='error')
        else:
            flash('Email not found!', category='error')

    # we can pass a variable to the template from our backend.
    # example passing variable user
    return render_template('login.html', user=current_user)


# define logout route
@auth.route('/logout')
# To make sure anyone can't access this without being logged in
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# define sign_up route
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # To check if the given email already exists.
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists!', category='error')

        # Form validations
        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 2 characters.', category='error')
        elif password1 != password2:
            flash('Password don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                password=generate_password_hash(password1, method='sha256')
            )
            # add the new user to the database.
            db.session.add(new_user)
            db.session.commit()

            # To log in the user and to crate a session into the flask web server
            # remember = true to remember the session in the browser memory.
            login_user(user, remember=True)

            flash('Account Created', category='success')
            # Pointing to the home function of views.py
            # Redirect to the home page.
            return redirect(url_for('views.home'))
    return render_template('sign_up.html', user=current_user)
