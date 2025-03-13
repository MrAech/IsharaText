from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from config import Config
from models.user import User

authBp = Blueprint('auth', __name__, template_folder='templates')


@authBp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('home.home'))
        else:
            flash('Invalid Username or Password', 'danger')

    return render_template('login.html')


@authBp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
        elif User.query.filter_by(email=email).first():
            flash('Email already exists.', 'danger')
        else:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            Config.getdb().session.add(new_user)
            Config.getdb().session.commit()
            flash('User created successfully.', 'success')
            return redirect(url_for('auth.login'))
        
    return render_template('signup.html')

@authBp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('auth.login'))