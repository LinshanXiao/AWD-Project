from flask import Blueprint, request, render_template, jsonify, send_file, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import pandas as pd
import os
import tempfile
from app.models import LeagueGame
from app import db
from app.forms import ManualUploadForm

upload_bp = Blueprint('upload_bp', __name__, url_prefix='/upload')

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# render the upload page
@upload_bp.route('/', methods=['GET'])
@login_required
def upload_page():
    form = ManualUploadForm()
    return render_template('upload.html', form=form)

# upload CSV file
@upload_bp.route('/csv', methods=['POST'])
@login_required
def upload_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename.lower()):
        temp_fd, temp_path = tempfile.mkstemp()
        try:
            with os.fdopen(temp_fd, 'wb') as f:
                f.write(file.read())

            with open(temp_path, 'r', encoding='utf-8') as f:
                df = pd.read_csv(f)

            result = process_csv(df)
            return jsonify(result), 200

        except Exception as e:
            return jsonify({'error': f'Error processing CSV: {str(e)}'}), 500

        finally:
            try:
                os.remove(temp_path)
            except Exception as unlink_err:
                print(f"⚠️ Failed to delete temp file: {unlink_err}")

    return jsonify({'error': 'Unsupported file type'}), 400

# process the CSV file
def process_csv(df):
    added, errors = 0, []

    for i, row in df.iterrows():
        try:
            k = int(row.get('kills', 0))
            d = int(row.get('deaths', 1))
            a = int(row.get('assists', 0))
            kda = round((k + a) / d, 1) if d > 0 else k + a

            new_record = LeagueGame(
                user_id=current_user.id,
                game_id=int(row['game_id']),
                date_played=pd.to_datetime(row['date_played']),
                game_duration=str(row['game_duration']),
                winning_team=row['winning_team'],
                league_username=row['league_username'],
                champion=row['champion'],
                kills=k,
                deaths=d,
                assists=a,
                kda=kda,
                team=row['team']
            )

            db.session.add(new_record)
            added += 1
        except Exception as e:
            errors.append(f"[Row {i+2}] {str(e)}")
            continue

    db.session.commit()

    return {
        'message': 'Upload completed.',
        'rows_added': added,
        'errors': errors
    }

# download the template CSV file
@upload_bp.route('/download-template')
@login_required
def download_template():
    template_path = os.path.join(current_app.root_path, 'static', 'template.csv')
    return send_file(template_path, as_attachment=True, download_name='template.csv')

# manual upload form
@upload_bp.route('/manual', methods=['POST'])
@login_required
def manual_upload():
    json_data = request.get_json()

    form = ManualUploadForm(data=json_data, meta={'csrf': False})  

    
    from flask_wtf.csrf import validate_csrf
    try:
        csrf_token = request.headers.get('X-CSRFToken')
        validate_csrf(csrf_token)
    except Exception as e:
        return jsonify({'error': 'CSRF validation failed', 'details': str(e)}), 400

    if form.validate():
        try:
            k = form.kills.data or 0
            d = form.deaths.data or 1
            a = form.assists.data or 0
            kda = round((k + a) / d, 1) if d > 0 else k + a

            new_record = LeagueGame(
                user_id=current_user.id,
                game_id=form.game_id.data,
                date_played=form.date_played.data,
                game_duration=str(form.game_duration.data),
                winning_team=form.winning_team.data,
                league_username=form.league_username.data,
                champion=form.champion.data,
                kills=k,
                deaths=d,
                assists=a,
                kda=kda,
                team=form.team.data
            )

            db.session.add(new_record)
            db.session.commit()

            return jsonify({'message': 'Manual upload successful'}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Upload failed: {str(e)}'}), 500
    else:
        errors = {field: ', '.join(msgs) for field, msgs in form.errors.items()}
        return jsonify({'error': 'Validation failed', 'details': errors}), 400


