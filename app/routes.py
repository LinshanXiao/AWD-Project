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

        # filter by username and password
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            # User is authenticated, set session or cookie here
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid username or password")

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
    # Assuming you want to display the first user in the database
    user = User.query.first()

    if user:
        return render_template('profile.html', user=user)
    else:
        return "No user found", 404

