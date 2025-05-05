from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


application = Flask(__name__)
application.config['SECRET_KEY'] = 'our_secret_key_here'

application.config.from_object(Config)
db = SQLAlchemy(application)
migrate = Migrate(application, db)


from app import routes, models








