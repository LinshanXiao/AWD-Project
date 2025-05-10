from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth_bp.login'  #  login route endpoint

def create_app():
    application = Flask(__name__)
    application.config.from_object(Config)
    application.secret_key = 'our_secret_key_here'

    # Bind extensions to app
    db.init_app(application)
    migrate.init_app(application, db)
    login_manager.init_app(application)

    # Register blueprints
    from app.auth.routes import auth_bp
    from app.main.routes import main_bp
    from app.upload.routes import upload_bp
    application.register_blueprint(auth_bp)
    application.register_blueprint(main_bp)
    application.register_blueprint(upload_bp)

    return application


from app.models import User

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)








