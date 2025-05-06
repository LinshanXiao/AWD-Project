from flask import render_template, request, redirect, url_for, flash
from app.models import User
from app import db
from app.auth import auth_bp
from flask_login import login_user,logout_user

#user login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:  
            login_user(user)  # flask automatic set sessions for us. 
            flash("Login successful!")
            return redirect(url_for('main_bp.home'))
        else:
            flash("Invalid username or password")
    return render_template("login.html")

# User register! 
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirmPassword')

        if password != confirm:
            flash("Passwords do not match.")
            return render_template('register.html')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already taken.")
            return render_template('register.html')

        newuser = User(username=username, email=email, password=password)
        db.session.add(newuser)
        db.session.commit()
        flash("Registration successful! Please log in.")
        return redirect(url_for('auth_bp.login'))

    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('main_bp.home'))


