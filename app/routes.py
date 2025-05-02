from app import application, db
from flask import render_template
from flask import request, redirect, url_for
from app.models import User, League_Game_Instance, League_Game_Player

@application.route('/')
@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == '1234':
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')

@application.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirmPassword')

        if password != confirm:
            return "Passwords do not match", 400

        newuser = User(username=username, email=email, password=password)
        db.session.add(newuser)
        db.session.commit()

        print(f"User registered: {username}, {email}")
        return redirect(url_for('login'))

    return render_template('register.html')

@application.route('/home')
def home():
    return render_template('home.html')

@application.route('/profile')
def profile():
    return "<h1>Profile page coming soon!</h1>"

