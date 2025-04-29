from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    username = db.Column(db.String(150), nullable=False, unique=True, primary_key=True)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    league_username = db.Column(db.String(150), nullable=True, unique=True)
    valorant_username = db.Column(db.String(150), nullable=True, unique=True)
    PUBG_username = db.Column(db.String(150), nullable=True, unique=True)
    apex_username = db.Column(db.String(150), nullable=True, unique=True)

class League_Game_Instance(db.Model):
    game_id = db.Column(db.Integer, primary_key=True)
    date_played = db.Column(db.DateTime, nullable=False)
    game_duration = db.Column(db.Time, nullable=False)
    winning_team = db.Column(db.String(150), nullable=False)

class League_Game_Player(db.Model):
    league_username = db.Column(db.String(150), db.ForeignKey('user.league_username'), primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('league_game_instance.game_id'), primary_key=True)
    champion = db.Column(db.String(150), nullable=False)
    kills = db.Column(db.Integer, nullable=False)
    deaths = db.Column(db.Integer, nullable=False)
    assists = db.Column(db.Integer, nullable=False)
    kda = db.Column(db.Float, nullable=False)
    team = db.Column(db.String(150), nullable=False)

User.league_games = db.relationship(
    'League_Game_Instance',
    secondary=League_Game_Player.__table__,
    backref='user',
    lazy='dynamic'
)