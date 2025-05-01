from app import application
from flask import render_template
from flask import request, redirect, url_for

@application.route('/')
@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Temporary login check
        if username == 'admin' and password == '1234':
            return redirect(url_for('main'))
        else:
            return "Invalid credentials", 401

    return render_template('login.html')

# Register route
@application.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')

        if password != confirm:
            return "Passwords do not match", 400
        
        # Simulate successful registration
        print(f"User registered: {username}, {email}")
        return redirect(url_for('login'))

    return render_template('register.html')

# Main (landing) page
@application.route('/main')
def main():
    return render_template('main.html')

