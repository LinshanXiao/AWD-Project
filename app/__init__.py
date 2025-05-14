from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

mail = Mail()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth_bp.login'  # Redirect if not logged in

def create_app():
    application = Flask(__name__)
    application.config.from_object('app.config.Config')

    db.init_app(application)
    migrate.init_app(application, db)
    login_manager.init_app(application)
    mail.init_app(application)

    from app.auth.routes import auth_bp
    from app.main.routes import main_bp
    from app.upload.routes import upload_bp
    application.register_blueprint(auth_bp)
    application.register_blueprint(main_bp)
    application.register_blueprint(upload_bp)

    return application

from app.models import User

@login_manager.user_loader
def load_user(user_id):  # ✅ use user_id here
    return User.query.get(int(user_id))
