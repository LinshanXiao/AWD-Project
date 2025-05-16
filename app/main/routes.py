from flask import render_template, session, redirect, url_for, flash,request,jsonify
from app.models import User, Friendship, LeagueGame, FriendRequest
from app.main import main_bp
from flask_login import login_required, current_user
from app import db
from datetime import datetime
from collections import defaultdict
import sqlalchemy as sa
import secrets
from PIL import Image
import os
from app.forms import UpdateProfileImageForm
from sqlalchemy import func
from collections import Counter



def save_profile_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join('app/static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@main_bp.route('/')
def index():
    return redirect(url_for('main_bp.home'))

@main_bp.route('/home')
def home():
    return render_template('home.html')


@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileImageForm()
    if form.validate_on_submit():
        if form.profile_image.data:
            picture_file = save_profile_picture(form.profile_image.data)
            current_user.profile_image = picture_file
            db.session.commit()
            flash('Profile image updated!', 'success')
            return redirect(url_for('main_bp.profile'))
        

    games = LeagueGame.query.filter_by(user_id=current_user.id).all()

    total_kills = sum(g.kills for g in games if g.kills is not None)
    total_deaths = sum(g.deaths for g in games if g.deaths is not None)
    total_assists = sum(g.assists for g in games if g.assists is not None)

    avg_kda = (
        round((total_kills + total_assists) / total_deaths, 2)
        if total_deaths > 0 else "∞"
    ) if games else "N/A"

    # ✅ Most played champion
    champion_counter = Counter(g.champion.strip().capitalize() for g in games)
    most_played = champion_counter.most_common(1)[0][0] if champion_counter else "N/A"

    return render_template(
        'profile.html',
        user=current_user,
        form=form,
        total_kills=total_kills,
        total_deaths=total_deaths,
        total_assists=total_assists,
        avg_kda=avg_kda,
        most_played=most_played
    )



@main_bp.route('/visualisation/<league_username>')
@login_required
def visualisation(league_username):

    user = User.query.filter_by(league_username=league_username).first()
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('main_bp.home'))
    
    # Ensure the user is either the current user or a friend
    if user.id == current_user.id:
        is_friend = True
    
    else:
        is_friend = Friendship.query.filter(
            ((Friendship.user_id == current_user.id) & (Friendship.friend_id == user.id)) |
            ((Friendship.user_id == user.id) & (Friendship.friend_id == current_user.id))
        ).first()
        if not is_friend:
            flash("You do not have permission to view this user's data.", "danger")
            return redirect(url_for('main_bp.home'))

    
    # Get the user's game data
    games = (
        LeagueGame.query
        .filter_by(league_username=league_username)
        .order_by(LeagueGame.date_played.desc())
        .all()
    )

    if not games:
        flash("You have no game data yet. Try uploading first.")
        return redirect(url_for('main_bp.home'))
    

    rows = []
    wins = 0
    champion_counts = defaultdict(int)
    win_counts = defaultdict(int)
    total_counts = defaultdict(int)

    for g in games:
        result = 'Win' if g.team == g.winning_team else 'Loss'
        if result == 'Win':
            wins += 1

        # prepare data for the table
        rows.append({
            'result': result,
            'champion': g.champion.capitalize(),
            'score': f"{g.kills}-{g.deaths}-{g.assists}",
            'date': g.date_played.strftime('%d/%m/%y'),
            'time': g.game_duration
        })

        # prepare data for the charts
        champ = g.champion.strip().capitalize()
        champion_counts[champ] += 1
        total_counts[champ] += 1
        if result == 'Win':
            win_counts[champ] += 1

    # win rate calculation
    win_rate = round((wins / len(games)) * 100, 1) if games else 0
    win_rates = {
        champ: round((win_counts[champ] / total_counts[champ]) * 100, 1)
        for champ in total_counts
    }

    # ✅ radar chart: compute average stats from all games
    if games:
        total_kills = sum(g.kills or 0 for g in games)
        total_deaths = sum(g.deaths or 0 for g in games)
        total_assists = sum(g.assists or 0 for g in games)
        total_kda = sum(((g.kills or 0) + (g.assists or 0)) / (g.deaths or 1) for g in games)
        total_impact = sum((g.kills or 0) + (g.assists or 0) for g in games)
        n = len(games)

        radar_data = {
            'Kills': round(total_kills / n, 1),
            'Deaths': round(max(0, 10 - (total_deaths / n)), 1),  
            'Assists': round(total_assists / n, 1),
            'KDA': round(total_kda / n, 2),
            'Impact': round(total_impact / n, 1)
        }
    else:
        radar_data = {}

    return render_template(
        'visualisation.html',
        rows=rows,
        total_wins=wins,
        win_rate=win_rate,
        champion_counts=dict(champion_counts),
        win_rates=win_rates,
        radar_data=radar_data,
        user=user  # ✅ pass to template
    )






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

    # Check if they are already friends
    existing_friendship = Friendship.query.filter(
        ((Friendship.user_id == current_user.id) & (Friendship.friend_id == friend_id)) |
        ((Friendship.user_id == friend_id) & (Friendship.friend_id == current_user.id))
    ).first()
    if existing_friendship:
        return jsonify({'message': 'You are already friends!'}), 400
    
    # Check if a pending friend request already exists
    existing_request = FriendRequest.query.filter_by(sender_id=current_user.id, receiver_id=friend_id).first()
    if existing_request:
        return jsonify({'message': 'Friend request already sent!'}), 400

    # check if the user exist
    friend = User.query.get(friend_id)
    if not friend:
        return jsonify({'message': 'User not found'}), 404

    # Create a new friend request
    new_request = FriendRequest(sender_id=current_user.id, receiver_id=friend_id)
    db.session.add(new_request)
    db.session.commit()

    return jsonify({'message': f'Friend request sent to {friend.username}!'}), 200


@main_bp.route('/account_settings', methods=['GET', 'POST'])
@login_required
def account_settings():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        email = request.form.get('email')
        league_username = request.form.get('league_username') 
        valorant_username = request.form.get('valorant_username') 
        PUBG_username = request.form.get('PUBG_username') 
        apex_username = request.form.get('apex_username') 

        # Update the current user's settings
        
        current_user.username = username
        current_user.email = email
        if league_username != '':
            current_user.league_username = league_username
        if valorant_username != '':
            current_user.valorant_username = valorant_username
        if PUBG_username != '':
            current_user.PUBG_username = PUBG_username
        if apex_username != '':
            current_user.apex_username = apex_username

        # Save changes to the database
        db.session.commit()
        flash('Account settings updated successfully!', 'success')
        return redirect(url_for('main_bp.account_settings'))

    return render_template('account_settings.html', user=current_user)


@main_bp.route('/accept_friend', methods=['POST'])
@login_required
def accept_friend():
    data = request.get_json()
    request_id = data.get('request_id')
    if not request_id:
        return jsonify({'message': 'Missing request ID'}), 400

    friend_request = FriendRequest.query.get(request_id)
    if (not friend_request) or (friend_request.receiver_id != current_user.id):
        return jsonify({'message': 'Friend request not found or not yours.'}), 404

    
    sender = friend_request.sender

    
    db.session.add(Friendship(user_id=current_user.id, friend_id=sender.id))
    db.session.add(Friendship(user_id=sender.id, friend_id=current_user.id))
    db.session.delete(friend_request)
    db.session.commit()

    
    return jsonify({
        'message': 'Friend request accepted!',
        'friend': {
            'id': sender.id,
            'username': sender.username,
            'league_username': sender.league_username
        }
    }), 200




@main_bp.route('/remove_friend', methods=['POST'])
@login_required
def remove_friend():
    data = request.get_json()
    friend_id = data.get('friend_id')

    if not friend_id:
        return jsonify({'message': 'Missing friend ID'}), 400

    # Find the friendship
    friendship_1 = Friendship.query.filter_by(user_id=current_user.id, friend_id=friend_id).first()
    friendship_2 = Friendship.query.filter_by(user_id=friend_id, friend_id=current_user.id).first()

    if not friendship_1 or not friendship_2:
        return jsonify({'message': 'Friendship not found'}), 404

    # Remove the friendship both ways
    db.session.delete(friendship_1)
    db.session.delete(friendship_2)
    db.session.commit()

    return jsonify({'message': 'Friend removed successfully!'}), 200



@main_bp.route('/decline_friend', methods=['POST'])
@login_required
def decline_friend():
    data = request.get_json()
    request_id = data.get('request_id')

    if not request_id:
        return jsonify({'message': 'Missing request ID'}), 400

    # Find the friend request
    friend_request = FriendRequest.query.get(request_id)
    if not friend_request:
        return jsonify({'message': 'Friend request not found'}), 404

    # Ensure the current user is the receiver of the request
    if friend_request.receiver_id != current_user.id:
        return jsonify({'message': 'You are not authorized to decline this request'}), 403

    # Remove the pending friend request
    db.session.delete(friend_request)
    db.session.commit()

    return jsonify({'message': 'Friend request declined!'}), 200



@main_bp.route('/notifications')
@login_required
def notifications():
    # Get pending friend requests
    friend_requests = FriendRequest.query.filter_by(receiver_id=current_user.id).all()

    # Get current friends
    current_friends = [
        {"id": friend.id, "username": friend.username, "league_username": friend.league_username}
        for friend in User.query.join(Friendship, Friendship.friend_id == User.id)
        .filter(Friendship.user_id == current_user.id)
        .all()
    ]

    return render_template(
        'notification_page.html',
        friend_requests=friend_requests,
        current_friends=current_friends
    )