from flask import render_template, session, redirect, url_for, flash
from app.models import User
from app.main import main_bp
from flask_login import login_required, current_user


@main_bp.route('/')
def index():
    return redirect(url_for('main_bp.home'))

@main_bp.route('/home')
def home():
    return render_template('home.html')


@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html',user=current_user)



@main_bp.route('/visualisation')
@login_required
def visualisation():
    return render_template('visualisation.html')
