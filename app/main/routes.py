from flask import render_template, session, redirect, url_for, flash,request,jsonify
from app.models import User,Friendship 
from app.main import main_bp
from flask_login import login_required, current_user
from app import db
import sqlalchemy as sa

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



@main_bp.route('/api/search_user')
@login_required
def search_user():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'found': False})

    # prevent adding yourself as friend.
    user = User.query.filter(
        (User.username.ilike(f'%{query}%')) | (User.id.cast(sa.String) == query)
    ).filter(User.id != current_user.id).first()

    if user:
        return jsonify({'found': True, 'id': user.id, 'username': user.username})
    else:
        return jsonify({'found': False})

@main_bp.route('/add_friend', methods=['POST'])
@login_required
def add_friend():
    data = request.get_json()
    friend_id = data.get('friend_id')

    if not friend_id:
        return jsonify({'message': 'Missing friend ID'}), 400

    if current_user.id == friend_id:
        return jsonify({'message': 'You cannot add yourself!'}), 400

    # check if they are friends both ways
    existing = Friendship.query.filter(
        ((Friendship.user_id == current_user.id) & (Friendship.friend_id == friend_id)) |
        ((Friendship.user_id == friend_id) & (Friendship.friend_id == current_user.id))
    ).first()
    if existing:
        return jsonify({'message': 'You are already friends!'}), 400

    # check if the user exist
    friend = User.query.get(friend_id)
    if not friend:
        return jsonify({'message': 'User not found'}), 404

    # add friendship
    new_friend = Friendship(user_id=current_user.id, friend_id=friend_id)
    db.session.add(new_friend)
    db.session.commit()

    return jsonify({'message': f'Add {friend.username} Successfully, you are friends now!'}), 200