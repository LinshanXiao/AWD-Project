from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, IntegerField
from wtforms.validators import DataRequired, Length, Optional

class ManualUploadForm(FlaskForm):
    class Meta:
        csrf=False  #delete this line of code  after we add a token athuentication
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
