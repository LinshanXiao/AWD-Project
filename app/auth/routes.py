from flask import render_template, redirect, url_for, flash,request,jsonify
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User
from app.auth import auth_bp
from app.forms import LoginForm, RegisterForm
from app.utils.email_utils import send_verification_code

# Login route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Login successful!")
            return redirect(url_for('main_bp.home'))
        else:
            flash("Invalid username or password.")
    return render_template("login.html", form=form)

# Register route
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data.lower(),
            email=form.email.data,
            password=hashed_pw
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.")
        return redirect(url_for('auth_bp.login'))
    return render_template("register.html", form=form)

from app.utils.email_utils import send_verification_code

@auth_bp.route('/send-verification', methods=['POST'])
def send_verification():
    email = request.form.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    send_verification_code(email)
    return jsonify({'message': 'Verification code sent.'}), 200

# Logout route
@auth_bp.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('main_bp.home'))


