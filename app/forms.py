from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,DateField, TimeField, IntegerField
from wtforms.validators import DataRequired,Email, EqualTo, Length, Optional,ValidationError
import re
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

# strong password validator
def strong_password(form, field):
    password = field.data
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters.")
    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password must include an uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise ValidationError("Password must include a lowercase letter.")
    if not re.search(r"\d", password):
        raise ValidationError("Password must include a number.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValidationError("Password must include a special character.")

# email domain validator
def valid_email_domain(form, field):
    allowed_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com','qq.com']
    # You can add more domains as needed
    domain = field.data.split('@')[-1]
    if domain not in allowed_domains:
        raise ValidationError("Please use a valid email provider like Gmail or Yahoo.")

# login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# register form
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email(), valid_email_domain])
    password = PasswordField('Password', validators=[DataRequired(), strong_password])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message="Passwords must match.")
    ])
    submit = SubmitField('Register')

    # username need to be unique
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already taken.")

    # email need to be unique
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered.")

class ManualUploadForm(FlaskForm):
    game_id = IntegerField('Game ID', validators=[DataRequired()])
    date_played = DateField('Date Played', format='%Y-%m-%d', validators=[DataRequired()])
    game_duration = TimeField('Game Duration', format='%H:%M:%S', validators=[DataRequired()])
    winning_team = StringField('Winning Team', validators=[DataRequired(), Length(max=150)])
    
    league_username = StringField('League Username', validators=[DataRequired(), Length(max=100)])
    champion = StringField('Champion', validators=[Optional()])
    kills = IntegerField('Kills', validators=[Optional()])
    deaths = IntegerField('Deaths', validators=[Optional()])
    assists = IntegerField('Assists', validators=[Optional()])
    team = StringField('Team', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Submit')
