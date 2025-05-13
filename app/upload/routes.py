from flask import Blueprint, request, render_template, jsonify, send_file, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import pandas as pd
import os
import tempfile
from app.models import League_Game_Instance, League_Game_Player
from app import db

upload_bp = Blueprint('upload_bp', __name__, url_prefix='/upload')

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'GET':
        return render_template('upload.html')

    if 'file' not in request.files:
        return jsonify({'error': 'There is no file section'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'File not selected'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        file.save(temp_file.name)

        try:
            df = pd.read_csv(temp_file.name)
            result = process_csv(df)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': f'An error occurred when processing CSV:: {str(e)}'}), 500
        finally:
            os.unlink(temp_file.name)

    return jsonify({'error': 'Unsupported file types'}), 400


def process_csv(df):
    added_game, updated_game = 0, 0
    added_player, updated_player = 0, 0
    errors = []

    for i, row in df.iterrows():
        try:
            game_id = int(row['game_id'])
            date_played = pd.to_datetime(row['date_played'])
            game_duration = pd.to_datetime(row['game_duration']).time()
            winning_team = row['winning_team']

            # game example processing 
            game = League_Game_Instance.query.get(game_id)
            if game:
                game.date_played = date_played
                game.game_duration = game_duration
                game.winning_team = winning_team
                updated_game += 1
            else:
                new_game = League_Game_Instance(
                    game_id=game_id,
                    date_played=date_played,
                    game_duration=game_duration,
                    winning_team=winning_team
                )
                db.session.add(new_game)
                added_game += 1

            # players data processing if exists 
            if 'league_username' in row and pd.notna(row['league_username']):
                league_username = row['league_username']
                player = League_Game_Player.query.get((league_username, game_id))

                player_data = {
                    'champion': row.get('champion'),
                    'kills': int(row.get('kills', 0)),
                    'deaths': int(row.get('deaths', 0)),
                    'assists': int(row.get('assists', 0)),
                    'kda': round((int(row.get('kills', 0)) + int(row.get('assists', 0))) / int(row.get('deaths', 1)), 1) if int(row.get('deaths', 1)) > 0 else int(row.get('kills', 0)) + int(row.get('assists', 0)),
                    'team': row.get('team')
                }

                if player:
                    for key, val in player_data.items():
                        setattr(player, key, val)
                    updated_player += 1
                else:
                    new_player = League_Game_Player(
                        league_username=league_username,
                        game_id=game_id,
                        **player_data
                    )
                    db.session.add(new_player)
                    added_player += 1

        except Exception as e:
            errors.append(f"Number of {i+2}row has error: {str(e)}")
            continue

    db.session.commit()

    return {
        'message': 'Upload Successful',
        'games_added': added_game,
        'games_updated': updated_game,
        'players_added': added_player,
        'players_updated': updated_player,
        'errors': errors
    }

@upload_bp.route('/download-template')
@login_required
def download_template():
    template_path = os.path.join(current_app.root_path, 'static', 'template.csv')
    return send_file(template_path, as_attachment=True, download_name='game_template.csv')


# Please feel free to remove all of this stuff
@upload_bp.route('/notifications')
@login_required
def notifications():
    friend_requests = [
        {"name": "Andy"},
        {"name": "John"},
        {"name": "Sarah"},
        {"name": "Andy"},
        {"name": "John"},
        {"name": "Sarah"},
        {"name": "Andy"},
        {"name": "John"},
        {"name": "Sarah"},
        {"name": "Andy"},
        {"name": "John"},
        {"name": "Sarah"}
    ]

    current_friends = [
        {"name": "Dirk"},
        {"name": "Yiming"},
        {"name": "Margot_Robbie"}
    ]
    return render_template('notification_page.html', friend_requests=friend_requests, current_friends=current_friends)
