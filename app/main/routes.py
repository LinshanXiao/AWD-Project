from flask import render_template, session, redirect, url_for, flash,request,jsonify
from app.models import User, Friendship, LeagueGame
from app.main import main_bp
from flask_login import login_required, current_user
from app import db
from datetime import datetime
from collections import defaultdict
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
    # Get the user's game data
    games = (
        LeagueGame.query
        .filter_by(user_id=current_user.id)
        .order_by(LeagueGame.date_played.desc())
        .all()
    )

    if not games:
        flash("You have no game data yet. Try uploading first.")

    rows = []
    wins = 0

    # collect data for the table and charts
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
        radar_data=radar_data
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
        if username:
            current_user.username = username
        if email:
            current_user.email = email
        if league_username:
            current_user.league_username = league_username
        if valorant_username:
            current_user.valorant_username = valorant_username
        if PUBG_username:
            current_user.PUBG_username = PUBG_username
        if apex_username:
            current_user.apex_username = apex_username

        # Save changes to the database
        db.session.commit()
        flash('Account settings updated successfully!', 'success')
        return redirect(url_for('main_bp.account_settings'))

    return render_template('account_settings.html', user=current_user)