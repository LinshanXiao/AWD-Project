from flask import render_template, session, redirect, url_for, flash,request,jsonify
from app.models import User,Friendship,LeagueGame
from app.main import main_bp
from flask_login import login_required, current_user
from app import db
from datetime import datetime
from sqlalchemy.orm import joinedload
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
    player_games = (
        LeagueGame.query
        .filter_by(league_username=current_user.league_username)
        .join(LeagueGame)
        .order_by(LeagueGame.date_played.desc())
        .all()
    )

    if not player_games:
        flash("You have no game data yet. Try uploading first.")

    # create game record data
    rows = []
    wins = 0
    for pg in player_games:
        game = pg.game
        result = 'Win' if pg.team == game.winning_team else 'Loss'
        if result == 'Win':
            wins += 1
        score = f"{pg.kills or 0}-{pg.deaths or 0}-{pg.assists or 0}"
        date = game.date_played.strftime('%d/%m/%y')
        time = game.game_duration.strftime('%H:%M:%S')
        rows.append({
            'result': result,
            'champion': pg.champion,
            'score': score,
            'date': date,
            'time': time
        })
        print(f"[DEBUG] Number of rows: {len(rows)}")


    total = len(player_games)
    win_rate = round((wins / total) * 100, 1) if total > 0 else 0

    return render_template(
        'visualisation.html',
        rows=rows,
        total_wins=wins,
        win_rate=win_rate
    )



@main_bp.route('/visualisation/<username>')
@login_required
def visualisation_data(username):
    # Get all player entries for the current user
    if username != current_user.username:
        # Check if the username is a friend of the current user
        is_friend = db.session.query(Friendship).filter(
            (Friendship.user_id == current_user.id) & 
            (Friendship.friend_id == User.query.filter_by(username=username).first().id)
        ).first()

        if not is_friend:
            flash("You do not have permission to view this user's data.", "danger")
            return redirect(url_for('main_bp.home'))
        

    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('main_bp.home'))
    

    player_games = (
        League_Game_Player.query
        .filter_by(league_username=user.league_username)
        .join(League_Game_Instance)
        .options(joinedload(League_Game_Player.game))
        .order_by(League_Game_Instance.date_played.asc())
        .all()
    )

    # Prepare data for charts
    score_labels = []
    score_data = []
    champion_stats = defaultdict(lambda: {'wins': 0, 'total': 0})

    for pg in player_games:
        game = pg.game
        if not game:
            continue

        # Line chart data (score over time)
        score = (pg.kills or 0) + (pg.assists or 0) - (pg.deaths or 0)
        label = game.date_played.strftime('%Y-%m-%d')
        score_labels.append(label)
        score_data.append(score)

        # Bar chart data (win rate per champion)
        champ = (pg.champion or 'Unknown').strip().lower()
        champion_stats[champ]['total'] += 1
        if pg.team == game.winning_team:
            champion_stats[champ]['wins'] += 1
        

    return render_template(
        'visualisation.html',
        user=user,
        score_labels=score_labels,
        score_data=score_data,
        champion_stats=champion_stats
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