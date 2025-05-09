# app.py
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import pandas as pd
import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Game, Base
import tempfile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}
app.config['MAX_CONTENT_LENGTH'] = 128 * 1024 * 1024 
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


DATABASE_URL = "sqlite:///xxxx.db"  
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'There is no file section.'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'Unselected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        file.save(temp_file.name)

        try:
            with open(temp_file.name, 'r', encoding='utf-8') as f:
                csv_reader = csv.reader(f)
                headers = next(csv_reader)

                required_columns = ['game_id']
                for column in required_columns:
                    if column not in headers:
                        return jsonify({'error': f'The CSV file is missing the necessary columns: {column}'}), 400

            result = process_csv(temp_file.name)
            return jsonify(result), 200

        except Exception as e:
            return jsonify({'error': f'An error occurred when processing CSV: {str(e)}'}), 500
        finally:
            os.unlink(temp_file.name)

    return jsonify({'error': 'Unsupported file types'}), 400


def process_csv(file_path):
    df = pd.read_csv(file_path)


    if 'game_id' not in df.columns:
        return {'error': 'CSV must contain the "game_id" column'}


    added = 0
    updated = 0
    errors = 0
    error_rows = []

    session = Session()
    try:

        for index, row in df.iterrows():
            try:

                if pd.isna(row['game_id']):
                    error_rows.append(f"Line {index + 2}: game_id is empty")
                    errors += 1
                    continue


                row_dict = {}
                for column in df.columns:
                    if not pd.isna(row[column]):
                        row_dict[column] = row[column]


                game_id = row_dict['game_id']
                existing_game = session.query(Game).filter_by(game_id=game_id).first()

                if existing_game:

                    for key, value in row_dict.items():
                        if key != 'id' and hasattr(existing_game, key):
                            setattr(existing_game, key, value)
                    updated += 1
                else:

                    new_game = Game(**row_dict)
                    session.add(new_game)
                    added += 1

            except Exception as e:
                error_rows.append(f"Line {index + 2}: {str(e)}")
                errors += 1


        session.commit()

        result = {
            'success': True,
            'message': f'CSV was successfully imported. added: {added}, updated: {updated}',
            'added': added,
            'updated': updated
        }

        if errors > 0:
            result['warnings'] = f'There is an error in line {errors} during the processing'
            result['error_details'] = error_rows

        return result

    except Exception as e:
        session.rollback()
        return {'error': f'An error occurred when updating the database: {str(e)}'}
    finally:
        session.close()


@app.route('/download-template')
def download_template():
    template_path = os.path.join(app.root_path, 'static', 'template.csv')
    return send_file(template_path, as_attachment=True, attachment_filename='game_template.csv')


if __name__ == '__main__':
    app.run(debug=True)