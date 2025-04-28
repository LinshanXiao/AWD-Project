from flask import Flask
from app.models import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'our_secret_key_here'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
from app import routes








